import sys
import os
sys.path.append(os.getcwd())

from app.agents.scout import ScoutAgent
import json
import logging

# Configure logging to stdout
logging.basicConfig(level=logging.INFO)

agent = ScoutAgent()
print("Attempting to collect data for TATAMOTORS.NS...")

try:
    # accessing the static method directly for easier debugging of the specific component
    print("Calling _get_financials_deep_static...")
    data = ScoutAgent._get_financials_deep_static("TATAMOTORS.NS")
    print("\nData collected successfully:")
    print(json.dumps(data, indent=2, default=str))
except Exception as e:
    print(f"\nFailed to collect data: {e}")
    import traceback
    traceback.print_exc()

print("\n---------------------------------------------------")
print("Calling _get_financials_deep_static for HDFCBANK.NS...")
try:
    data = ScoutAgent._get_financials_deep_static("HDFCBANK.NS")
    print("\nData collected successfully:")
    print(json.dumps(data, indent=2, default=str))
except Exception as e:
    print(f"\nFailed to collect data: {e}")
    traceback.print_exc()
