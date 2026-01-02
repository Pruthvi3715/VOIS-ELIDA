import requests
import json
import time

BASE_URL = "http://localhost:8000"
ASSET = "RELIANCE.NS"

def run_analysis():
    print(f"--- 🚀 Starting Analysis for {ASSET} ---")
    
    # 1. Ingest (Scout -> RAG)
    print(f"\n1. 📡 Ingesting Data (Scout)...")
    try:
        start_time = time.time()
        res = requests.post(f"{BASE_URL}/ingest/{ASSET}")
        elapsed = time.time() - start_time
        
        if res.status_code == 200:
            print(f"   ✅ Ingestion Complete ({elapsed:.2f}s)")
            print(f"   Response: {res.json()}")
        else:
            print(f"   ❌ Ingestion Failed: {res.status_code} - {res.text}")
            return
    except Exception as e:
        print(f"   ❌ Error connecting to backend: {e}")
        return

    # 2. Retrieve & Synthesize (Agents -> RAG -> Coach)
    print(f"\n2. 🧠 Running Multi-Agent Analysis (Strict RAG)...")
    try:
        start_time = time.time()
        # Query generic "comprehensive analysis" to trigger all agents
        res = requests.get(f"{BASE_URL}/retrieve?query=comprehensive%20analysis&asset_id={ASSET}")
        elapsed = time.time() - start_time
        
        if res.status_code == 200:
            data = res.json()
            print(f"   ✅ Analysis Complete ({elapsed:.2f}s)\n")
            
            # 3. Display Results
            print("--- 📊 COACH VERDICT ---")
            verdict = data.get("coach_verdict", {})
            print(f"Verdict: {verdict.get('verdict')}")
            print(f"Action:  {verdict.get('action')}")
            print(f"Conf:    {verdict.get('confidence')}%")
            
            print("\n--- 🕵️ RAG TRACEABILITY ---")
            print(f"Global Context Chunks: {data.get('global_context_count')}")
            print(f"Agent Insights Read:   {data.get('coach_retrieval_count')}")
            
            print("\n--- 🤖 AGENT OPINIONS ---")
            results = data.get("results", {})
            for agent, res in results.items():
                print(f"{agent.upper()}: {res.get('score') or res.get('trend') or res.get('risk_level')}")
                
        else:
            print(f"   ❌ Analysis Failed: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"   ❌ Error connecting to backend: {e}")

if __name__ == "__main__":
    run_analysis()
