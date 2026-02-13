import requests
import json

r = requests.get('http://localhost:8000/analyze/HDFCBANK.NS', timeout=120)
d = r.json()

print('=== MARKET DATA ===')
md = d.get('market_data', {})
print(f"Sector: {md.get('sector')}")
print(f"Industry: {md.get('industry')}")
print(f"Source: {md.get('source')}")
print(f"D/E: {md.get('debt_to_equity')}")
print(f"P/E: {md.get('pe_ratio')}")
print(f"ROE: {md.get('return_on_equity')}")

print()
print('=== MACRO DATA ===')
raw = d.get('raw_data', {}).get('macro', {})
print(f"Region: {raw.get('region')}")
print(f"VIX: {raw.get('volatility_index')}")
print(f"VIX Symbol: {raw.get('volatility_index_symbol')}")

print()
print('=== AGENT SCORES ===')
agents = d.get('agents', {})
for name, data in agents.items():
    output = data.get('output', {})
    score = output.get('score') or output.get('trend') or output.get('alignment') or output.get('risk_level') or output.get('action')
    conf = data.get('confidence', 'N/A')
    print(f"{name}: {score} (conf: {conf})")

# Save full response
with open('hdfc_test.json', 'w') as f:
    json.dump(d, f, indent=2, default=str)
print("\nSaved to hdfc_test.json")
