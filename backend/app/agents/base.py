from typing import List, Dict, Any, Callable, Optional
import os
import json
import re
import requests
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class BaseAgent:
    """
    Enhanced Base Agent with Ollama + Gemini support.
    
    LLM Provider Selection (via LLM_PROVIDER env var):
    - 'auto': Ollama first -> Gemini fallback (default)
    - 'ollama': Ollama only
    - 'gemini': Gemini only
    """
    
    # Configurable via environment
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # Token tracking (class level)
    _token_usage = {}
    
    def __init__(self, name: str):
        self.name = name
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = None
        self.default_confidence = 50
        
        # LLM Provider selection
        self.llm_provider = os.getenv("LLM_PROVIDER", "auto").lower()
        self.use_ollama = self.llm_provider in ("auto", "ollama")
        self.use_gemini = self.llm_provider in ("auto", "gemini")
        
        # Track token usage for this agent
        if self.name not in BaseAgent._token_usage:
            BaseAgent._token_usage[self.name] = {"input": 0, "output": 0, "calls": 0}
        
        # Check Ollama availability
        if self.use_ollama:
            try:
                resp = requests.get("http://localhost:11434/api/tags", timeout=2)
                if resp.status_code == 200:
                    print(f"[{self.name}] ✅ Ollama Available ({self.OLLAMA_MODEL})")
                else:
                    self.use_ollama = False
            except:
                self.use_ollama = False
                if self.llm_provider == "ollama":
                    print(f"[{self.name}] ❌ Ollama required but not running!")
                else:
                    print(f"[{self.name}] ⚠️ Ollama not running, will use Gemini")
        
        # Initialize Gemini
        if self.use_gemini and self.api_key and genai:
            try:
                genai.configure(api_key=self.api_key)
                self.gemini_model = genai.GenerativeModel(self.GEMINI_MODEL)
                if self.llm_provider == "gemini":
                    print(f"[{self.name}] ✅ Gemini ({self.GEMINI_MODEL}) Initialized.")
            except Exception as e:
                print(f"[{self.name}] ❌ Failed to init Gemini: {e}")

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (~4 chars per token for English)."""
        return len(text) // 4

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama local LLM."""
        try:
            response = requests.post(
                self.OLLAMA_URL,
                json={
                    "model": self.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120  # 2 min timeout for slower machines
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as e:
            print(f"[{self.name}] ⚠️ Ollama error: {e}")
        return None

    def call_llm(
        self, 
        prompt: str, 
        system_prompt: str = "You are a helpful financial analyst.", 
        fallback_func: Optional[Callable] = None, 
        fallback_args: Any = None,
        max_retries: int = 3
    ) -> str:
        """
        Calls LLM based on LLM_PROVIDER setting.
        Returns response and tracks token usage.
        """
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        input_tokens = self._estimate_tokens(full_prompt)
        
        result = None
        provider_used = None
        
        # Try Ollama first (if enabled)
        if self.use_ollama:
            print(f"[{self.name}] 🦙 Calling Ollama ({self.OLLAMA_MODEL})... (~{input_tokens} tokens)")
            result = self._call_ollama(full_prompt)
            if result:
                provider_used = "ollama"
                print(f"[{self.name}] ✅ Ollama Response: ~{self._estimate_tokens(result)} tokens")
            elif self.llm_provider == "ollama":
                # Ollama-only mode but failed
                print(f"[{self.name}] ❌ Ollama failed (no fallback in ollama-only mode)")
            else:
                print(f"[{self.name}] ⚠️ Ollama failed, trying Gemini...")
        
        # Try Gemini (if enabled and Ollama didn't succeed)
        if not result and self.use_gemini and self.gemini_model:
            try:
                print(f"[{self.name}] 🚀 Calling Gemini ({self.GEMINI_MODEL})... (~{input_tokens} tokens)")
                
                import time
                for attempt in range(max_retries):
                    try:
                        response = self.gemini_model.generate_content(full_prompt)
                        result = response.text
                        provider_used = "gemini"
                        print(f"[{self.name}] ✅ Gemini Response: ~{self._estimate_tokens(result)} tokens")
                        break
                    except Exception as e:
                        error_str = str(e)
                        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                            wait_time = (2 ** attempt) * 3
                            print(f"[{self.name}] ⚠️ Rate Limit. Retry {attempt+1}/{max_retries} in {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            raise e
                            
                if not result:
                    raise Exception(f"Max retries ({max_retries}) exceeded for Gemini API")

            except Exception as e:
                print(f"[{self.name}] ❌ Gemini Error: {e}. Using fallback.")
        
        # Track token usage
        if result:
            output_tokens = self._estimate_tokens(result)
            BaseAgent._token_usage[self.name]["input"] += input_tokens
            BaseAgent._token_usage[self.name]["output"] += output_tokens
            BaseAgent._token_usage[self.name]["calls"] += 1
            return result
        
        # Execute fallback
        if fallback_func:
            print(f"[{self.name}] 🔄 Using rule-based fallback")
            return fallback_func(fallback_args)
        return "[Error] Analysis unavailable - No LLM available and no fallback logic."
    
    @classmethod
    def get_token_usage(cls) -> Dict[str, Any]:
        """Get token usage statistics for all agents."""
        total_input = sum(a["input"] for a in cls._token_usage.values())
        total_output = sum(a["output"] for a in cls._token_usage.values())
        return {
            "by_agent": cls._token_usage,
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output
        }
    
    @classmethod
    def reset_token_usage(cls):
        """Reset token usage counters."""
        for agent in cls._token_usage:
            cls._token_usage[agent] = {"input": 0, "output": 0, "calls": 0}


    def format_output(
        self,
        output_data: Dict[str, Any],
        confidence: int = 50,
        data_quality: str = "Medium",
        fallback_used: bool = False,
        analysis: str = ""
    ) -> Dict[str, Any]:
        """
        Creates a standardized output format for all agents.
        """
        return {
            "agent": self.name,
            "timestamp": datetime.now().isoformat(),
            "output": output_data,
            "confidence": max(0, min(100, confidence)),
            "data_quality": data_quality,
            "fallback_used": fallback_used,
            "analysis": analysis
        }

    def parse_json_from_response(self, response: str) -> Optional[Dict]:
        """
        Attempts to extract JSON from LLM response.
        Handles various formats including markdown code blocks.
        """
        # Try direct JSON parse first
        try:
            return json.loads(response)
        except:
            pass
        
        # Try extracting from markdown code block
        json_patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, response)
            if match:
                try:
                    json_str = match.group(1) if '```' in pattern else match.group(0)
                    return json.loads(json_str)
                except:
                    continue
        
        return None

    def extract_score(self, response: str, default: int = 50) -> int:
        """
        Extracts numeric score from various response formats.
        """
        patterns = [
            r'["\']?score["\']?\s*[:=]\s*(\d+)',
            r'Score:\s*(\d+)',
            r'score\s+(?:is\s+)?(\d+)',
            r'\b(\d{1,3})\s*(?:/\s*100|%|points?)\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return max(0, min(100, score))
        
        return default

    def extract_confidence(self, response: str, default: int = 50) -> int:
        """
        Extracts confidence score from response.
        """
        patterns = [
            r'["\']?confidence["\']?\s*[:=]\s*(\d+)',
            r'Confidence:\s*(\d+)',
            r'confidence\s+(?:is\s+)?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                conf = int(match.group(1))
                return max(0, min(100, conf))
        
        return default

    def extract_level(self, response: str, levels: List[str], default: str = None) -> str:
        """
        Extracts a categorical level from response.
        Levels should be ordered from lowest to highest priority for matching.
        """
        if default is None:
            default = levels[len(levels) // 2]  # Middle level as default
        
        response_upper = response.upper()
        for level in reversed(levels):  # Check highest priority first
            if level.upper() in response_upper:
                return level
        
        return default

    def run(self, context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process the given context and return a result.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement run()")

    def calculate_data_quality(self, data: Any) -> str:
        """
        Calculates data quality rating based on completeness and relevance.
        Enhanced to check for critical fields if data is a dictionary.
        """
        if not data:
            return "Low"
        
        # Define critical fields for rudimentary check (can be specialized by agent)
        # This is a general heuristic
        critical_fields = ["symbol", "price", "market_cap", "pe_ratio", "revenue", "net_income"]
        
        quality_score = 0
        max_score = 10
        
        if isinstance(data, dict):
            # Check for non-null values
            non_null = sum(1 for v in data.values() if v is not None and v != "N/A" and v != "")
            total = len(data)
            completeness_ratio = non_null / total if total > 0 else 0
            
            # Base score from completeness
            quality_score += completeness_ratio * 5
            
            # Check for critical fields presence
            found_critical = sum(1 for f in critical_fields if f in data and data[f] not in [None, "N/A", ""])
            critical_ratio = found_critical / len(critical_fields)
            quality_score += critical_ratio * 5
            
        elif isinstance(data, list):
            # For lists (like news or history), check count and content
            if not data:
                return "Low"
                
            count = len(data)
            # 5+ items is good for lists like news/history
            count_score = min(5, count) 
            quality_score += count_score
            
            # Check if items are seemingly valid dicts
            valid_items = sum(1 for item in data if isinstance(item, dict) and len(item) > 1)
            validity_ratio = valid_items / count if count > 0 else 0
            quality_score += validity_ratio * 5
            
        else:
            # String or other primitive
            return "High" if data else "Low"
        
        # Determine final rating
        if quality_score >= 7.5:
            return "High"
        elif quality_score >= 4.0:
            return "Medium"
        else:
            return "Low"
