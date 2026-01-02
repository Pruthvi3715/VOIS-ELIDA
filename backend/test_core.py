import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.orchestrator import orchestrator

try:
    print("Ingesting AAPL...")
    res = orchestrator.ingest_asset("AAPL")
    print("Ingestion result:", res.keys())
    
    # print("Retrieving context...")
    # analysis = orchestrator.retrieve_context("analysis", "AAPL")
    # print("Analysis result keys:", analysis.keys())
    # print("Match Score:", analysis.get("match_score"))

except Exception as e:
    import traceback
    traceback.print_exc()
