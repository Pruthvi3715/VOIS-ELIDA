import sys
import os
import requests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth.auth import create_access_token

# 1. Generate Token for User 1
token = create_access_token(data={"sub": "1"}) # Keeping original token generation as the instruction's line was syntactically incorrect and would cause a NameError.
print(f"Generated Token: {token[:20]}...")

# 2. Call API
print("\nCalling http://localhost:8000/analyze/ITC.NS...")
headers = {"Authorization": f"Bearer {token}"}

try:
    response = requests.get("http://localhost:8000/analyze/ITC.NS", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("\nAPI Response:")
        print(f"  Score: {data.get('match_score')}")
        print(f"  Recommendation: {data.get('recommendation')}")
        
        # Debug prints for keys
        print(f"Top-level keys: {list(data.keys())}")
        if "results" in data:
             print(f"Results keys: {list(data['results'].keys())}")
             if "match_score" in data["results"]:
                 print(f"Match Score keys: {list(data['results']['match_score'].keys())}")
        
        # Check inside match_result if typical response structure differs
        mr = data.get('match_result', {})
        if mr:
             print(f"  MR Recommendation: {mr.get('recommendation')}")
             
        # Check specific concerns
        concerns = data.get('match_result', {}).get('concern_reasons', [])
        print(f"  Concerns: {concerns}")
        
        # Check market data
        if response.status_code == 200:
            data = response.json()
            market_data = data.get("market_data", {})
            results = data.get("results", {})
            match_score = results.get("match_score", {})
            
            print("\n✅ Analysis Successful")
            print(f"Match Score: {match_score.get('match_score')}")
            print(f"Confidence: {match_score.get('breakdown', {}).get('confidence_level')}")
            print("\n--- Breakdown ---")
            breakdown = match_score.get("breakdown", {})
            print(f"Fundamental: {breakdown.get('fundamental_score')} (Weight: {breakdown.get('fundamental_weight')})")
            print(f"Macro:       {breakdown.get('macro_score')} (Weight: {breakdown.get('macro_weight')})")
            print(f"Philosophy:  {breakdown.get('philosophy_score')} (Weight: {breakdown.get('philosophy_weight')})")
            print(f"Risk:        {breakdown.get('risk_score')} (Weight: {breakdown.get('risk_weight')})")
            print(f"DNA Match:   {breakdown.get('dna_match_score')} (Weight: {breakdown.get('dna_weight')})")
            print("-----------------")
            
            print(f"\n--- Market Data Check ---")
            print(f"Market Data Keys: {list(market_data.keys())}")
            
            history = market_data.get("history", [])
            print(f"History Type: {type(history)}")
            print(f"History Length: {len(history)}")
            
            if len(history) > 0:
                print(f"Sample History Item Keys: {list(history[0].keys())}")
                print(f"Sample Item: {history[0]}")
            else:
                print("⚠️  No history found in market_data")
                # Check technicals just in case
                tech_history = market_data.get("technicals", {}).get("history", [])
                print(f"Technicals History Length: {len(tech_history)}")
            
            print("-----------------")
except Exception as e:
    print(f"Request failed: {e}")
