import requests
import time
import json

URL = "http://localhost:8000/analyze/AAPL"

def verify_latency():
    print(f"Sending request to {URL}...")
    start_time = time.time()
    
    try:
        response = requests.get(URL, params={"demo": "false"})
        end_time = time.time()
        
        latency = end_time - start_time
        print(f"\nResponse Time: {latency:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print("Status: 200 OK")
            
            # Check if it looks like a valid analysis
            if "investment_thesis" in data:
                print("Content: Valid Analysis Received")
                print(f"Thesis: {data.get('investment_thesis', '')[:100]}...")
            else:
                print("Content: JSON received but key fields missing.")
                print(f"Keys: {list(data.keys())}")
        else:
            print(f"Status: {response.status_code}")
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    verify_latency()
