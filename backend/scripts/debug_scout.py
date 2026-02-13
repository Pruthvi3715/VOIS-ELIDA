import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.scout import scout_agent

print("Fetching data for MSFT...")
data = scout_agent.collect_data("MSFT")

history = data.get("financials", {}).get("history", [])
financials = data.get("financials", {})
print(f"Source: {financials.get('source')}")
print(f"History items: {len(history)}")

print("\n--- Advanced Metrics Check ---")
advanced_keys = ["enterprise_value", "price_to_sales", "enterprise_to_ebitda", "shares_outstanding", "float_shares", "held_percent_insiders", "fiscal_year_ends"]
for key in advanced_keys:
    print(f"{key}: {financials.get(key)}")
print("------------------------------\n")

if history:
    print("First history item:", history[0])
else:
    print("No history found in financials.")

technicals = data.get("technicals", {})
tech_history = technicals.get("history", [])
print(f"Technical history items: {len(tech_history)}")

# Check structure matches what frontend expects
# Frontend looks for analysis.market_data.history or analysis.market_data.technicals.history
