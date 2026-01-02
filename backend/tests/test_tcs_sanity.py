"""Test script for TCS.NS sanity checker."""
import sys
sys.path.insert(0, '.')

from app.services.cache_service import clear_cache
clear_cache()

from app.agents.scout import scout_agent

print("=" * 60)
print("TCS.NS SANITY CHECK TEST")
print("=" * 60)

result = scout_agent.collect_data('TCS.NS')

print("\n--- FINANCIALS ---")
f = result['financials']
print(f"Symbol: {f.get('symbol')}")
print(f"Sector: {f.get('sector')}")
print(f"Industry: {f.get('industry')}")
print(f"D/E Ratio: {f.get('debt_to_equity')}")
print(f"D/E Corrected: {f.get('debt_to_equity_corrected', False)}")
if f.get('debt_to_equity_corrected'):
    print(f"  Original D/E: {f.get('debt_to_equity_original')}")
print(f"P/E Ratio: {f.get('pe_ratio')}")
print(f"Profit Margins: {f.get('profit_margins')}")

print("\n--- SANITY ALERTS ---")
alerts = result.get('sanity_alerts', [])
if alerts:
    for a in alerts:
        print(f"[{a['severity']}] {a['field']}: {a['message']}")
else:
    print("No sanity alerts - data looks clean!")

print("\n✅ Test complete")
