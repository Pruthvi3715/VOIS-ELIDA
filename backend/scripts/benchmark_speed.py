import sys, os
sys.path.append(os.getcwd())
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

from app.orchestrator import FinancialOrchestrator
import time

from app.agents.scout import scout_agent

orch = FinancialOrchestrator()
symbol = 'SUZLON.NS'
print(f"Running benchmark for {symbol} (Parallel Execution)...")

start = time.time()
try:
    # 1. Collect & Ingest (Setup)
    print("Step 1: Collection & Ingestion...")
    # ingest_asset handles collection internally
    orch.ingest_asset(symbol)
    
    # 2. Analyze (The part we optimized)
    print("Step 2: Analysis (Agents)...")
    analysis_start = time.time()
    # retrieve_context triggers the agent analysis pipeline if context is retrieved
    result = orch.retrieve_context(
        query=f"Analysis of {symbol}",
        asset_id=symbol
    )
    
    analysis_elapsed = time.time() - analysis_start
    total_elapsed = time.time() - start
    
    print(f"\n✅ Analysis Phase Complete in {analysis_elapsed:.2f} seconds")
    print(f"Total Pipeline Time: {total_elapsed:.2f} seconds")
    
    print(f"Match Score: {result.get('match_score')}")
    print(f"Recommendation: {result.get('match_result', {}).get('recommendation')}")
    
    # Check if we got results
    if 'results' in result:
        print("\nAgent Status:")
        for agent, res in result['results'].items():
            status = "✅ OK" if res else "❌ Empty"
            print(f"  - {agent.capitalize()}: {status}")

except Exception as e:
    print(f"\n❌ Benchmark Failed: {e}")
    import traceback
    traceback.print_exc()
