"""
Simple TSLA Stock Analysis using Groq API
Runs a comprehensive analysis on Tesla stock.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
ASSET = "TSLA"  # Tesla stock symbol

def run_analysis():
    print(f"\n{'='*60}")
    print(f"🚀 TSLA (Tesla) Stock Analysis using Groq API")
    print(f"{'='*60}\n")
    
    # 1. Ingest (Scout -> RAG)
    print(f"📡 Step 1: Ingesting Data for {ASSET}...")
    try:
        start_time = time.time()
        res = requests.post(f"{BASE_URL}/ingest/{ASSET}", timeout=60)
        elapsed = time.time() - start_time
        
        if res.status_code == 200:
            print(f"   ✅ Ingestion Complete ({elapsed:.2f}s)")
            data = res.json()
            if "metrics" in data:
                metrics = data["metrics"]
                print(f"\n   📊 Key Metrics:")
                print(f"      • Current Price: ${metrics.get('current_price', 'N/A')}")
                print(f"      • Market Cap: ${metrics.get('market_cap', 'N/A'):,}" if isinstance(metrics.get('market_cap'), (int, float)) else f"      • Market Cap: {metrics.get('market_cap', 'N/A')}")
                print(f"      • P/E Ratio: {metrics.get('pe_ratio', 'N/A')}")
                print(f"      • 52W High: ${metrics.get('52w_high', 'N/A')}")
                print(f"      • 52W Low: ${metrics.get('52w_low', 'N/A')}")
        else:
            print(f"   ❌ Ingestion Failed: {res.status_code} - {res.text}")
            return
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Error: Backend server not running at {BASE_URL}")
        print(f"   Please start the backend with: cd backend && uvicorn app.main:app --reload")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # 2. Run Multi-Agent Analysis
    print(f"\n🧠 Step 2: Running Multi-Agent Analysis (Groq API)...")
    try:
        start_time = time.time()
        res = requests.get(
            f"{BASE_URL}/retrieve",
            params={"query": "comprehensive stock analysis", "asset_id": ASSET},
            timeout=120
        )
        elapsed = time.time() - start_time
        
        if res.status_code == 200:
            data = res.json()
            print(f"   ✅ Analysis Complete ({elapsed:.2f}s)\n")
            
            # 3. Display Coach Verdict
            print(f"{'='*60}")
            print("📋 COACH VERDICT (AI Investment Recommendation)")
            print(f"{'='*60}")
            verdict = data.get("coach_verdict", {})
            print(f"   • Verdict:    {verdict.get('verdict', 'N/A')}")
            print(f"   • Action:     {verdict.get('action', 'N/A')}")
            print(f"   • Confidence: {verdict.get('confidence', 'N/A')}%")
            print(f"   • Summary:    {verdict.get('summary', 'N/A')[:200]}..." if verdict.get('summary') else "")
            
            # 4. Display Agent Opinions
            print(f"\n{'='*60}")
            print("🤖 AGENT ANALYSIS BREAKDOWN")
            print(f"{'='*60}")
            results = data.get("results", {})
            
            agent_info = {
                "quant": ("📊 Quant Agent", "Technical/Quantitative Analysis"),
                "macro": ("🌍 Macro Agent", "Macroeconomic Factors"),
                "philosopher": ("🧘 Philosopher Agent", "Long-term Value & Ethics"),
                "regret": ("⚠️ Regret Agent", "Risk & Regret Analysis")
            }
            
            for agent_key, (agent_name, description) in agent_info.items():
                if agent_key in results:
                    agent_data = results[agent_key]
                    print(f"\n{agent_name} - {description}")
                    print(f"   • Score/Rating: {agent_data.get('score') or agent_data.get('trend') or agent_data.get('risk_level', 'N/A')}")
                    if agent_data.get('reasoning'):
                        reasoning = agent_data['reasoning'][:300]
                        print(f"   • Reasoning: {reasoning}...")
            
            # 5. RAG Traceability
            print(f"\n{'='*60}")
            print("🔍 RAG TRACEABILITY")
            print(f"{'='*60}")
            print(f"   • Global Context Chunks: {data.get('global_context_count', 'N/A')}")
            print(f"   • Agent Insights Read:   {data.get('coach_retrieval_count', 'N/A')}")
            
            print(f"\n{'='*60}")
            print("✅ Analysis Complete!")
            print(f"{'='*60}\n")
            
        else:
            print(f"   ❌ Analysis Failed: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"   ❌ Error during analysis: {e}")

if __name__ == "__main__":
    run_analysis()
