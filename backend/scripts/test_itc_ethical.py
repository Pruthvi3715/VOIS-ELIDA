import sys
import os
import json
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.getcwd())

# Force reload of env vars
load_dotenv(override=True)

try:
    from app.orchestrator import orchestrator
    from app.models.investor_dna import InvestorDNA
    from app.services.match_score_service import match_score_service
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_itc_tobacco_exclusion():
    asset_id = "ITC.NS"
    print(f"\n🚀 Starting Ethical Filter Test for {asset_id}")
    
    # 1. Setup Investor DNA with Tobacco Exclusion
    profile = InvestorDNA(
        user_id="test_user_tobacco",
        risk_tolerance="moderate",
        investment_style="value",
        exclude_tobacco=True,
        custom_rules=["I DONT WANT TOBACCO COMPANY"]
    )
    
    print(f"Profile: {profile.dict()}")
    
    # 2. Ingest Data (Scout + RAG)
    print(f"\n📡 Ingesting data for {asset_id}...")
    ingest_result = orchestrator.ingest_asset(asset_id)
    print(f"Ingest Status: {ingest_result.get('status')}")
    
    # 3. Retrieve Analysis (Agent reasoning + Match Score)
    print(f"\n🧠 Running full agent analysis and match score calculation...")
    analysis = orchestrator.retrieve_context(
        query="comprehensive analysis",
        asset_id=asset_id,
        investor_dna=profile
    )
    
    # 4. Results Check
    match_result = analysis.get("match_result", {})
    match_score = match_result.get("score", 0)
    recommendation = match_result.get("recommendation", "N/A")
    concern_reasons = match_result.get("concern_reasons", [])
    
    print("\n" + "="*50)
    print(f"RESULT FOR {asset_id}")
    print(f"Match Score: {match_score}%")
    print(f"Recommendation: {recommendation}")
    print(f"Concerns: {concern_reasons}")
    print("="*50)
    
    # Validation logic
    tobacco_warn = any("tobacco" in r.lower() or "ethics" in r.lower() or "preferences" in r.lower() for r in concern_reasons)
    
    if tobacco_warn and recommendation == "Avoid":
        print("\n✅ TEST PASSED: Tobacco company correctly identified and excluded.")
    else:
        print("\n❌ TEST FAILED: Tobacco exclusion logic did not trigger as expected.")
        if not tobacco_warn:
            print("Reason: No tobacco-related warning in concerns.")
        if recommendation != "Avoid":
            print(f"Reason: Recommendation was {recommendation} instead of Avoid.")

if __name__ == "__main__":
    test_itc_tobacco_exclusion()
