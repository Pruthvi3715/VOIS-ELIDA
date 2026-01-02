import requests
import json
import sys

URL = "http://localhost:8000/analyze/SUZLON.NS"
print(f"Calling {URL}...")
try:
    resp = requests.get(URL, timeout=120)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Keys:", list(data.keys()))
        
        if "match_result" in data:
            print("match_result keys:", list(data["match_result"].keys()))
            if "breakdown" in data["match_result"]:
                print("breakdown:", data["match_result"]["breakdown"])
        else:
            print("MISSING 'match_result' key!")
            
        if "market_data" in data:
            print("market_data keys:", list(data["market_data"].keys()))
            history = data["market_data"].get("history", [])
            print(f"History length: {len(history)}")
            if history:
                print("First history item:", history[0])
        else:
            print("MISSING 'market_data' key!")
            
        if "results" in data:
            print("Agent results keys:", list(data["results"].keys()))
            
    else:
        print("Error response:", resp.text)
except Exception as e:
    print(f"Request failed: {e}")
