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


from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("agents.base")

class BaseAgent:
    """
    Enhanced Base Agent with multi-provider LLM support.
    
    LLM Provider Selection (via settings):
    - 'auto': Groq first -> Ollama -> Gemini fallback
    - 'groq': Groq only (fast cloud, llama-3.3-70b)
    - 'ollama': Ollama only (local)
    - 'gemini': Gemini only (Google cloud)
    """
    
    # Configurable via environment (read at call time for hot-reload)
    OLLAMA_URL = "http://localhost:11434/api/generate"
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    OPENROUTER_URL = "https://openrouter.ai/api/v1"
    
    @property
    def ollama_model(self):
        """Read OLLAMA_MODEL from settings."""
        return settings.OLLAMA_MODEL
    
    @property
    def gemini_model_name(self):
        """Read GEMINI_MODEL from settings."""
        return settings.GEMINI_MODEL
    
    @property
    def groq_model(self):
        """Read GROQ_MODEL from settings."""
        return settings.GROQ_MODEL
    
    @property
    def groq_api_key(self):
        """Read GROQ_API_KEY from settings."""
        return settings.GROQ_API_KEY
        
    @property
    def openrouter_model(self):
        """Read OPENROUTER_MODEL from settings."""
        return settings.OPENROUTER_MODEL
        
    @property
    def openrouter_api_key(self):
        """Read OPENROUTER_API_KEY from settings."""
        return settings.OPENROUTER_API_KEY
    
    # Token tracking (class level)
    _token_usage = {}
    
    def __init__(self, name: str):
        self.name = name
        self.api_key = settings.GEMINI_API_KEY
        self.gemini_model = None
        self.default_confidence = 50
        
        # LLM Provider selection
        self.llm_provider = settings.LLM_PROVIDER.lower()
        self.use_groq = self.llm_provider in ("auto", "groq")
        self.use_ollama = self.llm_provider in ("auto", "ollama")
        self.use_gemini = self.llm_provider in ("auto", "gemini")
        self.use_openrouter = self.llm_provider in ("auto", "openrouter")
        
        # Track token usage for this agent
        if self.name not in BaseAgent._token_usage:
            BaseAgent._token_usage[self.name] = {"input": 0, "output": 0, "calls": 0}
    
    def get_guardrail_system_prompt(self, base_prompt: str) -> str:
        """
        Add anti-hallucination guardrails to any system prompt.
        All agents should use this method to wrap their system prompts.
        """
        guardrails = """

CRITICAL GUARDRAILS - YOU MUST FOLLOW THESE:
1. ONLY use data explicitly provided in the context. Do NOT invent numbers, facts, or metrics.
2. If data is missing or insufficient, say "Insufficient data for [X]" instead of guessing.
3. NEVER mention or analyze any company/stock other than the one specified in the context.
4. If unsure about any assessment, reduce your confidence score accordingly (below 50 for major uncertainty).
5. CITE specific numbers from the provided data in your reasoning to prove you're using real data.
6. If the data looks suspicious, anomalous, or inconsistent, FLAG it rather than using it blindly.
7. Do NOT hallucinate historical events, news, or market movements not present in the data.
"""
        return f"{base_prompt}\n{guardrails}"
        
        # Check Groq availability
        if self.use_groq and self.groq_api_key:
            logger.info(f"[{self.name}] [OK] Groq Available ({self.groq_model})")
        elif self.llm_provider == "groq":
            logger.error(f"[{self.name}] [ERROR] Groq requires GROQ_API_KEY in .env!")
            self.use_groq = False

        # Check Ollama availability
        if self.use_ollama:
            try:
                resp = requests.get("http://localhost:11434/api/tags", timeout=2)
                if resp.status_code == 200:
                    if self.llm_provider == "ollama":
                        logger.info(f"[{self.name}] [OK] Ollama Available ({self.ollama_model})")
                else:
                    self.use_ollama = False
            except:
                self.use_ollama = False
                if self.llm_provider == "ollama":
                    logger.error(f"[{self.name}] [ERROR] Ollama required but not running!")

        # Initialize Gemini
        if self.use_gemini and self.api_key and genai:
            try:
                genai.configure(api_key=self.api_key)
                self.gemini_model = genai.GenerativeModel(self.gemini_model_name)
                if self.llm_provider == "gemini":
                    logger.info(f"[{self.name}] [OK] Gemini ({self.gemini_model_name}) Initialized.")
            except Exception as e:
                logger.error(f"[{self.name}] [ERROR] Failed to init Gemini: {e}")

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (~4 chars per token for English)."""
        return len(text) // 4

    def _call_groq(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Call Groq API with rate limit handling and retries."""
        import time
        
        if not self.groq_api_key:
            return None
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.GROQ_URL,
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.groq_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 2048
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                
                elif response.status_code == 429:
                    # Rate limit - extract wait time or use exponential backoff
                    wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                    retry_after = response.headers.get("retry-after")
                    if retry_after:
                        wait_time = min(int(retry_after), 30)  # Cap at 30s
                    
                    logger.warning(f"[{self.name}] ⏳ Groq rate limit. Waiting {wait_time}s (attempt {attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                    
                else:
                    logger.error(f"[{self.name}] [WARN] Groq error: {response.status_code} - {response.text[:100]}")
                    return None
                    
            except Exception as e:
                logger.error(f"[{self.name}] [WARN] Groq error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
        
        logger.error(f"[{self.name}] [ERROR] Groq rate limit exceeded after {max_retries} retries")
        return None

    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama local LLM."""
        try:
            response = requests.post(
                self.OLLAMA_URL,
                json={
                    "model": self.ollama_model,  # Now reads from env at call time
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300  # 5 min timeout for larger models (14B)
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as e:
            logger.error(f"[{self.name}] [WARN] Ollama error: {e}")
        return None

    def _call_gemini(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Call Gemini API with retries."""
        if not self.gemini_model:
            return None
            
        import time
        for attempt in range(max_retries):
            try:
                # Synchronous call for now
                response = self.gemini_model.generate_content(prompt)
                if response.text:
                    return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait_time = (2 ** attempt) * 2
                    logger.warning(f"[{self.name}] [WARN] Gemini Rate Limit. Retry {attempt+1}/{max_retries} in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"[{self.name}] [WARN] Gemini Error: {e}")
                    # Don't retry on non-transient errors usually, but loop continues
                    if attempt == max_retries - 1:
                        return None
        return None

    def _call_openrouter(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Call OpenRouter API."""
        if not self.openrouter_api_key:
            return None
            
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url=self.OPENROUTER_URL,
                api_key=self.openrouter_api_key,
            )
            
            response = client.chat.completions.create(
                model=self.openrouter_model,
                messages=[{"role": "user", "content": prompt}],
                # extra_body={"reasoning": {"enabled": True}} # Enable if model supports it, configurable?
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"[{self.name}] [ERROR] OpenRouter Error: {e}")
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
        Calls LLM with fallback strategy: OpenRouter -> Groq -> Ollama -> Gemini -> Rule-based Fallback.
        """
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
        input_tokens = self._estimate_tokens(full_prompt)
        
        result = None
        provider_used = None
        
        # 0. Try OpenRouter (if enabled)
        if self.use_openrouter and self.openrouter_api_key:
            logger.info(f"[{self.name}] 🦄 Calling OpenRouter ({self.openrouter_model})...")
            result = self._call_openrouter(full_prompt)
            if result:
                provider_used = "openrouter"
                logger.info(f"[{self.name}] [OK] OpenRouter Response")
            else:
                 logger.warning(f"[{self.name}] [WARN] OpenRouter failed/empty.")
                 
        # 1. Try Groq first (fast cloud)
        if not result and self.use_groq and self.groq_api_key:
            logger.info(f"[{self.name}] [CALL] Calling Groq ({self.groq_model})...")
            result = self._call_groq(full_prompt)
            if result:
                provider_used = "groq"
                logger.info(f"[{self.name}] [OK] Groq Response")
            else:
                logger.warning(f"[{self.name}] [WARN] Groq failed/empty.")
        
        # 2. Try Ollama (if configured and no result yet)
        if not result and self.use_ollama:
            logger.info(f"[{self.name}] 🦙 Calling Ollama ({self.ollama_model})...")
            result = self._call_ollama(full_prompt)
            if result:
                provider_used = "ollama"
                logger.info(f"[{self.name}] [OK] Ollama Response")
            else:
                logger.warning(f"[{self.name}] [WARN] Ollama failed/empty.")

        # 3. Try Gemini (if enabled and no result yet)
        if not result and self.use_gemini:
            logger.info(f"[{self.name}] 🚀 Calling Gemini ({self.gemini_model_name})...")
            result = self._call_gemini(full_prompt, max_retries)
            if result:
                provider_used = "gemini"
                logger.info(f"[{self.name}] [OK] Gemini Response")
            else:
                logger.error(f"[{self.name}] [ERROR] Gemini Failed.")

        # 3. Track Usage & Return
        if result:
            output_tokens = self._estimate_tokens(result)
            BaseAgent._token_usage[self.name]["input"] += input_tokens
            BaseAgent._token_usage[self.name]["output"] += output_tokens
            BaseAgent._token_usage[self.name]["calls"] += 1
            return result
        
        # 4. Final Fallback
        if fallback_func:
            logger.warning(f"[{self.name}] [RETRY] Using rule-based fallback")
            return fallback_func(fallback_args)
            
        # 5. No recourse
        return "[Error] Analysis unavailable - LLM generation failed and no fallback provided."
    
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
