"""
LLM Provider Comparison Script
Tests all available LLM providers and compares:
- Response time
- Output quality
- Reliability
"""

import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Test prompt - financial analysis
TEST_PROMPT = """Analyze this financial data and return JSON only:

DATA:
{
    "symbol": "TCS.NS",
    "company_name": "Tata Consultancy Services",
    "pe_ratio": 28.5,
    "return_on_equity": 0.45,
    "debt_to_equity": 8.2,
    "profit_margins": 0.215,
    "market_cap": "14.5T",
    "sector": "Technology"
}

OUTPUT FORMAT:
{
    "score": 0-100,
    "confidence": 0-100,
    "reasoning": "2-3 sentences",
    "strengths": ["list"],
    "weaknesses": ["list"]
}

SCORING: 0-40=Poor, 40-60=Fair, 60-80=Good, 80-100=Excellent
"""

SYSTEM_PROMPT = "You are a strict Quantitative Analyst. Output valid JSON only. Justify every score with specific metrics from the provided data."

results = {}

def test_ollama():
    """Test Ollama local LLM"""
    print("\n" + "="*60)
    print("🦙 TESTING OLLAMA (Local)")
    print("="*60)
    
    model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    
    print(f"Model: {model}")
    print(f"URL: {url}")
    
    # Check if Ollama is running
    try:
        check = requests.get("http://localhost:11434/api/tags", timeout=2)
        if check.status_code != 200:
            print("❌ Ollama NOT running!")
            return None
        print("✅ Ollama is running")
    except:
        print("❌ Ollama NOT running!")
        return None
    
    full_prompt = f"System: {SYSTEM_PROMPT}\n\nUser: {TEST_PROMPT}"
    
    start_time = time.time()
    try:
        response = requests.post(
            url,
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json().get("response", "")
            print(f"\n⏱️  Response Time: {elapsed:.2f}s")
            print(f"📝 Response Length: {len(result)} chars")
            print(f"\n📄 Output:\n{result[:500]}...")
            
            return {
                "provider": "Ollama",
                "model": model,
                "time": elapsed,
                "status": "✅ SUCCESS",
                "response": result,
                "response_length": len(result)
            }
        else:
            print(f"❌ Error: {response.status_code}")
            return {"provider": "Ollama", "model": model, "status": "❌ FAILED", "error": response.text}
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"provider": "Ollama", "model": model, "status": "❌ FAILED", "error": str(e)}


def test_groq():
    """Test Groq cloud LLM"""
    print("\n" + "="*60)
    print("⚡ TESTING GROQ (Cloud)")
    print("="*60)
    
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    print(f"Model: {model}")
    
    if not api_key:
        print("❌ GROQ_API_KEY not set!")
        return None
    print("✅ API Key found")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    full_prompt = f"System: {SYSTEM_PROMPT}\n\nUser: {TEST_PROMPT}"
    
    start_time = time.time()
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": full_prompt}],
                "temperature": 0.7,
                "max_tokens": 1024
            },
            timeout=60
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            print(f"\n⏱️  Response Time: {elapsed:.2f}s")
            print(f"📝 Response Length: {len(result)} chars")
            print(f"\n📄 Output:\n{result[:500]}...")
            
            return {
                "provider": "Groq",
                "model": model,
                "time": elapsed,
                "status": "✅ SUCCESS",
                "response": result,
                "response_length": len(result)
            }
        else:
            print(f"❌ Error: {response.status_code} - {response.text[:200]}")
            return {"provider": "Groq", "model": model, "status": "❌ FAILED", "error": response.text[:200]}
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"provider": "Groq", "model": model, "status": "❌ FAILED", "error": str(e)}


def test_gemini():
    """Test Gemini cloud LLM"""
    print("\n" + "="*60)
    print("🚀 TESTING GEMINI (Cloud)")
    print("="*60)
    
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    print(f"Model: {model}")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not set!")
        return None
    print("✅ API Key found")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel(model)
        
        full_prompt = f"System: {SYSTEM_PROMPT}\n\nUser: {TEST_PROMPT}"
        
        start_time = time.time()
        response = gemini_model.generate_content(full_prompt)
        elapsed = time.time() - start_time
        
        if response.text:
            result = response.text
            print(f"\n⏱️  Response Time: {elapsed:.2f}s")
            print(f"📝 Response Length: {len(result)} chars")
            print(f"\n📄 Output:\n{result[:500]}...")
            
            return {
                "provider": "Gemini",
                "model": model,
                "time": elapsed,
                "status": "✅ SUCCESS",
                "response": result,
                "response_length": len(result)
            }
        else:
            print("❌ Empty response")
            return {"provider": "Gemini", "model": model, "status": "❌ FAILED", "error": "Empty response"}
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"provider": "Gemini", "model": model, "status": "❌ FAILED", "error": str(e)}


def print_comparison(results):
    """Print comparison table"""
    print("\n" + "="*70)
    print("📊 LLM PROVIDER COMPARISON RESULTS")
    print("="*70)
    
    print(f"\n{'Provider':<15} {'Model':<25} {'Time':<10} {'Status':<12}")
    print("-"*70)
    
    for name, r in results.items():
        if r:
            time_str = f"{r.get('time', 0):.2f}s" if r.get('time') else "N/A"
            print(f"{r['provider']:<15} {r['model']:<25} {time_str:<10} {r['status']:<12}")
    
    print("\n" + "="*70)
    print("🏆 RECOMMENDATION FOR PRESENTATION:")
    print("="*70)
    
    # Find fastest successful
    successful = {k: v for k, v in results.items() if v and v.get('status') == '✅ SUCCESS'}
    
    if successful:
        fastest = min(successful.items(), key=lambda x: x[1]['time'])
        print(f"\n⚡ FASTEST: {fastest[1]['provider']} ({fastest[1]['time']:.2f}s)")
        
        # Evaluate quality (simple heuristic - JSON parseable, reasonable length)
        best_quality = None
        for name, r in successful.items():
            resp = r.get('response', '')
            if '{' in resp and '}' in resp and len(resp) > 200:
                if not best_quality or r['response_length'] > best_quality['response_length']:
                    best_quality = r
        
        if best_quality:
            print(f"📊 BEST QUALITY: {best_quality['provider']} ({best_quality['response_length']} chars)")
        
        print("\n🎯 FINAL RECOMMENDATION:")
        
        # Prefer Groq for speed in presentations
        if 'Groq' in successful:
            print("   USE GROQ for tomorrow's presentation!")
            print("   - Fastest cloud response (~1-3s)")
            print("   - Reliable API")
            print("   - Good quality output")
        elif 'Ollama' in successful:
            print("   USE OLLAMA for tomorrow's presentation!")
            print("   - Works offline (no internet needed)")
            print("   - No API rate limits")
            print("   - Privacy - data stays local")
        else:
            print(f"   USE {list(successful.keys())[0]} for tomorrow's presentation!")
    else:
        print("\n❌ No LLM providers working! Fix before presentation.")


if __name__ == "__main__":
    print("\n🧪 ELIDA LLM PROVIDER COMPARISON TEST")
    print("="*60)
    print(f"Current LLM_PROVIDER in .env: {os.getenv('LLM_PROVIDER', 'not set')}")
    print("="*60)
    
    results["ollama"] = test_ollama()
    results["groq"] = test_groq()
    results["gemini"] = test_gemini()
    
    print_comparison(results)
