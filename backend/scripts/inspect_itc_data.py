import sys
import os
sys.path.append(os.getcwd())

from app.agents.scout import scout_agent
import json

asset_id = "ITC.NS"
print(f"Fetching raw scout data for {asset_id}...")
data = scout_agent.collect_data(asset_id)

financials = data.get("financials", {})
print("\n--- Financials Data ---")
print(f"Sector: {financials.get('sector')}")
print(f"Industry: {financials.get('industry')}")
print(f"Full Financials Sample: {json.dumps(financials, indent=2)[:500]}")

sector = financials.get("sector", "").lower()
industry = financials.get("industry", "").lower()
combined = f"{sector} {industry}"
print(f"\nCombined string for matching: '{combined}'")
print(f"Match 'tobacco': {'tobacco' in combined}")
print(f"Match 'cigarette': {'cigarette' in combined}")
