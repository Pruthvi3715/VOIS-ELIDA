"""
Test the complete analysis flow with Groq LLM
"""
import sys
sys.path.append(".")

from app.orchestrator import orchestrator

def test_full_analysis(asset_id="RELIANCE.NS"):
    print(f"Testing full analysis for {asset_id}...")
    print("="*80)

    # Step 1: Ingest
    print("\n[1] Ingesting data...")
    ingest_result = orchestrator.ingest_asset(asset_id)
    print(f"Status: {ingest_result.get('status')}")

    # Step 2: Analyze
    print("\n[2] Running multi-agent analysis...")
    analysis_result = orchestrator.retrieve_context(
        query=f"Analyze {asset_id}",
        asset_id=asset_id
    )

    # Step 3: Display Results
    print("\n" + "="*80)
    print("ANALYSIS RESULTS")
    print("="*80)

    print(f"\nMATCH SCORE: {analysis_result.get('match_score')}/100")

    match_result = analysis_result.get('match_result', {})
    print(f"\nRecommendation: {match_result.get('recommendation')}")
    print(f"If you own: {match_result.get('action_if_owned')}")
    print(f"If you don't own: {match_result.get('action_if_not_owned')}")

    print(f"\n--- WHY IT FITS ---")
    for reason in match_result.get('fit_reasons', []):
        print(f"  + {reason}")

    print(f"\n--- CONCERNS ---")
    for reason in match_result.get('concern_reasons', []):
        print(f"  - {reason}")

    # Agent Results
    results = analysis_result.get('results', {})

    print("\n" + "="*80)
    print("AGENT ANALYSIS")
    print("="*80)

    # Quant Agent
    quant = results.get('quant', {})
    print(f"\n[QUANT AGENT]")
    print(f"  Score: {quant.get('score')}")
    print(f"  Confidence: {quant.get('confidence')}%")
    print(f"  Analysis: {quant.get('analysis', '')[:300]}...")

    # Macro Agent
    macro = results.get('macro', {})
    print(f"\n[MACRO AGENT]")
    print(f"  Trend: {macro.get('output_data', {}).get('trend')}")
    print(f"  Confidence: {macro.get('confidence')}%")
    print(f"  Analysis: {macro.get('analysis', '')[:300]}...")

    # Coach Verdict
    coach = analysis_result.get('coach_verdict', {})
    print(f"\n[COACH'S VERDICT]")
    print(f"  {coach.get('analysis', '')[:400]}...")

    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asset_id = sys.argv[1] if len(sys.argv) > 1 else "RELIANCE.NS"
    test_full_analysis(asset_id)
