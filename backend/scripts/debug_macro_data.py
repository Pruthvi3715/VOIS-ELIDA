import sys
import os

# Add backend to path (need to go up one level from scripts)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.scout import ScoutAgent

def test_macro_data():
    print("--- Testing Scout Agent Macro Data Collection ---")
    
    # Test for US Asset
    print("\nTesting for US Asset (MSFT)...")
    try:
        macro_us = ScoutAgent._get_macro_data_static("MSFT")
        print("Keys returned:", list(macro_us.keys()))
        print(f"VIX: {macro_us.get('volatility_index')}")
        print(f"10Y Yield: {macro_us.get('interest_rate_proxy')}")
        print(f"SPY Change: {macro_us.get('market_change_pct')}")
    except Exception as e:
        print(f"Error fetching US macro data: {e}")

    # Test for Indian Asset
    print("\nTesting for Indian Asset (ITC.NS)...")
    try:
        macro_in = ScoutAgent._get_macro_data_static("ITC.NS")
        print("Keys returned:", list(macro_in.keys()))
        print(f"India VIX: {macro_in.get('volatility_index')}")
        print(f"10Y Yield (India): {macro_in.get('interest_rate_proxy')}")
        print(f"Nifty Change: {macro_in.get('market_change_pct')}")
        print(f"RBI Repo Rate: {macro_in.get('rbi_repo_rate')}")
    except Exception as e:
        print(f"Error fetching India macro data: {e}")

if __name__ == "__main__":
    test_macro_data()
