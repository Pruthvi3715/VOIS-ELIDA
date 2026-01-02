"""
Integration test for Match Score with fresh data ingestion.
"""
import json
import sys
sys.path.insert(0, '.')

from app.services.cache_service import clear_cache

print("Clearing cache for fresh data...")
clear_cache()

from app.orchestrator import orchestrator
from app.models.investor_dna import InvestorDNA, RiskTolerance, InvestmentStyle

print("=" * 70)
print("MATCH SCORE INTEGRATION TEST (With Fresh Data)")
print("=" * 70)

# First, ingest fresh data
print("\n[STEP 1] Ingesting fresh data for ITC.NS")
print("-" * 50)
ingest_result = orchestrator.ingest_asset("ITC.NS")
print(f"Ingestion status: {ingest_result['status']}")
print(f"Data quality: {ingest_result.get('data_quality', {}).get('overall', 'Unknown')}")

# Test 1: Default investor profile
print("\n\n[TEST 1] Analyzing with DEFAULT investor profile")
print("-" * 50)

result1 = orchestrator.retrieve_context(
    query="comprehensive analysis",
    asset_id="ITC.NS",
    investor_dna=None
)

print(f"\n💯 Match Score: {result1['match_score']}%")
print(f"📊 Recommendation: {result1['match_result']['recommendation']}")

print("\n✅ Fit Reasons:")
for r in result1['match_result']['fit_reasons'][:3]:
    print(f"   • {r}")

print("\n⚠️ Concerns:")
for r in result1['match_result']['concern_reasons'][:3]:
    print(f"   • {r}")

# Test 2: Ethical investor who excludes tobacco
print("\n\n[TEST 2] Analyzing with TOBACCO-EXCLUDING investor")
print("-" * 50)

ethical_investor = InvestorDNA(
    user_id="ethical_investor",
    risk_tolerance=RiskTolerance.MODERATE,
    investment_style=InvestmentStyle.VALUE,
    exclude_tobacco=True
)

result2 = orchestrator.retrieve_context(
    query="comprehensive analysis",
    asset_id="ITC.NS",
    investor_dna=ethical_investor
)

print(f"\n💯 Match Score: {result2['match_score']}%")
print(f"📊 Recommendation: {result2['match_result']['recommendation']}")

print("\n⚠️ Concerns (should show tobacco exclusion):")
for r in result2['match_result']['concern_reasons']:
    print(f"   • {r}")

print(f"\n📝 Summary: {result2['match_result']['summary']}")

# Test 3: Conservative dividend investor
print("\n\n[TEST 3] Analyzing with CONSERVATIVE DIVIDEND investor")
print("-" * 50)

dividend_investor = InvestorDNA(
    user_id="dividend_investor",
    risk_tolerance=RiskTolerance.CONSERVATIVE,
    investment_style=InvestmentStyle.DIVIDEND,
    min_dividend_yield=2.0,
    prefer_profitable=True
)

result3 = orchestrator.retrieve_context(
    query="comprehensive analysis",
    asset_id="ITC.NS",
    investor_dna=dividend_investor
)

print(f"\n💯 Match Score: {result3['match_score']}%")
print(f"📊 Recommendation: {result3['match_result']['recommendation']}")
print(f"\n📝 Summary: {result3['match_result']['summary']}")

# Summary
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
Investor Type          | Match Score | Recommendation
-----------------------|-------------|---------------
Default (Moderate)     | {result1['match_score']:>11}% | {result1['match_result']['recommendation']}
Ethical (No Tobacco)   | {result2['match_score']:>11}% | {result2['match_result']['recommendation']}
Conservative Dividend  | {result3['match_score']:>11}% | {result3['match_result']['recommendation']}
""")

# Save results
output = {
    "asset": "ITC.NS",
    "sector": "Consumer Defensive / Tobacco",
    "tests": {
        "default_investor": {
            "match_score": result1['match_score'],
            "recommendation": result1['match_result']['recommendation'],
            "fit_reasons": result1['match_result']['fit_reasons'],
            "concerns": result1['match_result']['concern_reasons']
        },
        "ethical_investor": {
            "match_score": result2['match_score'],
            "recommendation": result2['match_result']['recommendation'],
            "fit_reasons": result2['match_result']['fit_reasons'],
            "concerns": result2['match_result']['concern_reasons']
        },
        "dividend_investor": {
            "match_score": result3['match_score'],
            "recommendation": result3['match_result']['recommendation'],
            "fit_reasons": result3['match_result']['fit_reasons'],
            "concerns": result3['match_result']['concern_reasons']
        }
    }
}

with open("match_score_test_results.json", 'w') as f:
    json.dump(output, f, indent=2)
print("✅ Results saved to match_score_test_results.json")
