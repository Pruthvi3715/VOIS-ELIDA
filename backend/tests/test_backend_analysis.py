import requests
import json
import time

BASE_URL = "http://localhost:8000"
TICKER = "TCS.NS"

def test_analysis():
    print(f"🚀 Testing Backend Analysis for {TICKER}...")
    
    # Analyze (One-Shot)
    print(f"\n1️⃣  Running One-Shot Analysis (/analyze/{TICKER})...")
    try:
        start = time.time()
        res = requests.get(f"{BASE_URL}/analyze/{TICKER}")
        print(f"   Status: {res.status_code}")
        print(f"   Time: {time.time() - start:.2f}s")
        
        if res.status_code == 200:
            data = res.json()
            
            # Check Match Score
            match = data.get("match_result", {})
            score = match.get("total_score")
            print(f"\n✅ Match Score: {score}")
            
            # Check Agents
            results = data.get("results", {})
            print(f"   Quant Agent: {'OK' if results.get('quant') else 'EMPTY'}")
            print(f"   Macro Agent: {'OK' if results.get('macro') else 'EMPTY'}")
            print(f"   Philosopher: {'OK' if results.get('philosopher') else 'EMPTY'}")
            
            if score is None:
                print("\n⚠️  Warning: Match Score is missing. Printing full response for debug:")
                print(json.dumps(data, indent=2)[:1000]) 
            else:
                 print("\nSample Agent Output (Quant):")
                 print(json.dumps(results.get("quant", {}), indent=2))

        else:
            print(f"   ❌ Error: {res.text}")

    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

if __name__ == "__main__":
    test_analysis()
