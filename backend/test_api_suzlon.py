"""Test API endpoint for SUZLON.NS"""
import requests
import json
import time

print("="*80)
print("Testing ELIDA API with SUZLON.NS")
print("="*80)

# Step 1: Ingest
print("\n[1/2] Ingesting SUZLON.NS data...")
ingest_response = requests.post(
    "http://localhost:8000/api/v1/analysis/ingest",
    json={"asset_id": "SUZLON.NS"}
)

print(f"Status Code: {ingest_response.status_code}")
if ingest_response.status_code == 200:
    print("✓ Ingestion successful")
    print(f"Response: {json.dumps(ingest_response.json(), indent=2)[:300]}...")
else:
    print(f"✗ Ingestion failed: {ingest_response.text}")
    exit(1)

# Step 2: Analyze
print("\n[2/2] Running multi-agent analysis...")
print("(This will take ~30-60 seconds...)")

analyze_response = requests.post(
    "http://localhost:8000/api/v1/analysis/analyze",
    json={
        "query": "Analyze SUZLON.NS",
        "asset_id": "SUZLON.NS"
    },
    timeout=120
)

print(f"Status Code: {analyze_response.status_code}")

if analyze_response.status_code == 200:
    result = analyze_response.json()

    print("\n" + "="*80)
    print("✓ ANALYSIS SUCCESSFUL!")
    print("="*80)

    print(f"\n📊 MATCH SCORE: {result.get('match_score')}/100")

    match_result = result.get('match_result', {})
    print(f"\n✓ Recommendation: {match_result.get('recommendation')}")
    print(f"  - If you own: {match_result.get('action_if_owned')}")
    print(f"  - If you don't own: {match_result.get('action_if_not_owned')}")

    print(f"\n--- WHY IT FITS ---")
    for reason in match_result.get('fit_reasons', [])[:3]:
        print(f"  + {reason}")

    print(f"\n--- CONCERNS ---")
    for reason in match_result.get('concern_reasons', [])[:3]:
        print(f"  - {reason}")

    # Agent scores
    results = result.get('results', {})
    print(f"\n--- AGENT SCORES ---")
    print(f"  Quant: {results.get('quant', {}).get('score')} (Confidence: {results.get('quant', {}).get('confidence')}%)")
    print(f"  Macro: Trend={results.get('macro', {}).get('output_data', {}).get('trend')} (Confidence: {results.get('macro', {}).get('confidence')}%)")

    print("\n" + "="*80)
    print("✓ YOUR FRONTEND SHOULD NOW WORK!")
    print("="*80)

else:
    print(f"\n✗ Analysis failed: {analyze_response.text}")
    exit(1)
