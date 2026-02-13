import requests
import json

# Test with a stock NOT in demo cache: TATAMOTORS.NS
r = requests.get('http://localhost:8000/analyze/TATAMOTORS.NS', timeout=180)
d = r.json()

print('=== RESULT ===')
print(f"orchestration_id: {d.get('orchestration_id')}")  # Should NOT say "demo_"
print(f"asset_id: {d.get('asset_id')}")

print()
print('=== MARKET DATA ===')
md = d.get('market_data', {})
print(f"Sector: {md.get('sector')}")
print(f"Industry: {md.get('industry')}")
print(f"Source: {md.get('source')}")
print(f"D/E: {md.get('debt_to_equity')}")
print(f"P/E: {md.get('pe_ratio')}")

print()
print('=== RAW DATA CHECK ===')
raw = d.get('raw_data', {})
if raw:
    financials = raw.get('financials', {})
    print(f"Financials Source: {financials.get('source')}")
    print(f"Financials Sector: {financials.get('sector')}")
    macro = raw.get('macro', {})
    print(f"Macro Region: {macro.get('region')}")
    print(f"Macro VIX Symbol: {macro.get('volatility_index_symbol')}")

print()
print('=== AGENT SCORES ===')
agents = d.get('agents', {})
if agents:
    for name, data in agents.items():
        output = data.get('output', {})
        score = output.get('score') or output.get('trend') or output.get('alignment') or output.get('risk_level') or output.get('action')
        conf = data.get('confidence', 'N/A')
        print(f"{name}: {score} (conf: {conf})")
else:
    print("No agents found - checking results dict")
    results = d.get('results', {})
    for name, data in results.items():
        print(f"{name}: {data}")

# Save full response
with open('tatamotors_test.json', 'w') as f:
    json.dump(d, f, indent=2, default=str)
print("\nSaved to tatamotors_test.json")
