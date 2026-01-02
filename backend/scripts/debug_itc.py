from app.agents.scout import scout_agent
import json

print("Fetching ITC.NS data...")
data = scout_agent.collect_data("ITC.NS")

print("\n--- Financials ---")
print(json.dumps(data.get("financials", {}), indent=2))

print("\n--- Technicals ---")
print(json.dumps(data.get("technicals", {}), indent=2))
