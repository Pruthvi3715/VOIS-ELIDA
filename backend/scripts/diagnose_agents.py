"""
Diagnostic script to test individual agents and identify issues.
"""
import sys, os
sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv(override=True)

print("="*60)
print("ELIDA AGENT DIAGNOSTIC TEST")
print("="*60)

# Check environment
print("\n[1] ENVIRONMENT CHECK:")
llm_provider = os.getenv("LLM_PROVIDER", "auto")
groq_key = os.getenv("GROQ_API_KEY")
print(f"  LLM_PROVIDER: {llm_provider}")
print(f"  GROQ_API_KEY: {'Set (' + groq_key[:10] + '...)' if groq_key else 'NOT SET'}")
print(f"  GROQ_MODEL: {os.getenv('GROQ_MODEL', 'not set')}")

# Test Groq directly
print("\n[2] DIRECT GROQ API TEST:")
import requests
try:
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            "messages": [{"role": "user", "content": "Say 'I am working' only"}],
            "max_tokens": 20
        },
        timeout=15
    )
    if resp.status_code == 200:
        print(f"  [OK] Groq API working: {resp.json()['choices'][0]['message']['content']}")
    else:
        print(f"  [ERROR] Groq API failed: {resp.status_code} - {resp.text[:100]}")
except Exception as e:
    print(f"  [ERROR] Groq connection failed: {e}")

# Test each agent
print("\n[3] INDIVIDUAL AGENT TESTS:")
from app.agents.quant import quant_agent
from app.agents.macro import macro_agent  
from app.agents.philosopher import philosopher_agent
from app.agents.regret import regret_agent

# Minimal test context
test_context = [{
    "content": "{'symbol': 'TEST', 'sector': 'Technology', 'pe_ratio': 25, 'debt_to_equity': 0.5, 'current_price': 100, 'market_cap': 1000000000}",
    "metadata": {"type": "financials"}
}]

agents = [
    ("Quant", quant_agent),
    ("Macro", macro_agent),
    ("Philosopher", philosopher_agent),
    ("Regret", regret_agent)
]

for name, agent in agents:
    print(f"\n  Testing {name} Agent...")
    try:
        result = agent.run(test_context)
        fallback = result.get('fallback_used', 'N/A')
        confidence = result.get('confidence', 'N/A')
        analysis_preview = result.get('analysis', '')[:100]
        
        status = "[FALLBACK]" if fallback else "[OK]"
        print(f"    {status} Confidence: {confidence}, Fallback: {fallback}")
        print(f"    Analysis: {analysis_preview}...")
    except Exception as e:
        print(f"    [ERROR] Agent failed: {e}")

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)
