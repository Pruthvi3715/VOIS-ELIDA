"""
DEBUG SCRIPT: Agent Data Flow Issue
This script traces the exact data flow to identify why agents receive empty context.
"""

import sys
sys.path.append(".")

from app.orchestrator import orchestrator
from app.services.rag_service import rag_service
import json

def debug_data_flow(asset_id: str = "RELIANCE.NS"):
    """Debug the complete data flow from Scout to Agents."""

    print("=" * 80)
    print(f"DEBUGGING DATA FLOW FOR: {asset_id}")
    print("=" * 80)

    # Step 1: Ingest Data
    print("\n[STEP 1] Ingesting data via Scout...")
    try:
        ingest_result = orchestrator.ingest_asset(asset_id)
        print(f"[OK] Ingestion Status: {ingest_result.get('status')}")
        print(f"   Asset ID: {ingest_result.get('asset_id')}")
    except Exception as e:
        print(f"[ERROR] Ingestion failed: {e}")
        return

    # Step 2: Check Cached Data
    print("\n[STEP 2] Checking orchestrator cache...")
    cached_data = orchestrator.current_asset_data.get(asset_id, {})
    if cached_data:
        print(f"[OK] Cached data exists:")
        print(f"   - Financials: {'YES' if cached_data.get('financials') else 'NO'}")
        print(f"   - Technicals: {'YES' if cached_data.get('technicals') else 'NO'}")
        print(f"   - Macro: {'YES' if cached_data.get('macro') else 'NO'}")

        # Show sample financial data
        if cached_data.get('financials'):
            fin = cached_data['financials']
            print(f"\n   Sample Financials:")
            print(f"   - PE Ratio: {fin.get('pe_ratio')}")
            print(f"   - Profit Margins: {fin.get('profit_margins')}")
            print(f"   - Debt/Equity: {fin.get('debt_to_equity')}")
    else:
        print("[ERROR] NO cached data found in orchestrator!")
        return

    # Step 3: Query RAG
    print("\n[STEP 3] Querying RAG for stored data...")
    rag_result = rag_service.query(
        query_text=f"Financial analysis of {asset_id}",
        n_results=10,
        where={"asset_id": asset_id}
    )

    if rag_result and rag_result.get('documents'):
        doc_count = len(rag_result['documents'][0])
        print(f"[OK] RAG returned {doc_count} documents")

        # Show metadata types
        if rag_result.get('metadatas'):
            types = [m.get('type') for m in rag_result['metadatas'][0] if m.get('type')]
            print(f"   Document types found: {set(types)}")

            # Show sample content
            for i, (doc, meta) in enumerate(zip(rag_result['documents'][0][:3], rag_result['metadatas'][0][:3])):
                print(f"\n   Doc {i+1} (type: {meta.get('type')}):")
                print(f"   Content preview: {doc[:150]}...")
    else:
        print("[ERROR] RAG returned EMPTY results!")
        print("   This means data was NOT stored or query failed.")

    # Step 4: Simulate Context Building (like orchestrator does)
    print("\n[STEP 4] Simulating orchestrator context building...")
    global_context = []

    # From RAG
    if rag_result and rag_result.get('documents'):
        for i, doc in enumerate(rag_result['documents'][0]):
            meta = rag_result['metadatas'][0][i] if rag_result.get('metadatas') else {}
            global_context.append({"content": doc[:2500], "metadata": meta})

    # From Direct Cache (orchestrator.py lines 141-161)
    if cached_data:
        if cached_data.get("financials"):
            global_context.append({
                "content": str(cached_data["financials"]),
                "metadata": {"asset_id": asset_id, "type": "financials", "source": "direct_cache"}
            })
        if cached_data.get("macro"):
            global_context.append({
                "content": str(cached_data["macro"]),
                "metadata": {"asset_id": "GLOBAL", "type": "macro", "source": "direct_cache"}
            })

    print(f"[OK] Built context with {len(global_context)} items")

    # Step 5: Filter for Agent Contexts (like quant.py:69 does)
    print("\n[STEP 5] Filtering context for agents...")

    # Quant Agent Filter
    financial_data = [c for c in global_context if c.get("metadata", {}).get("type") == "financials"]
    print(f"   Quant Agent would receive: {len(financial_data)} financial items")
    if not financial_data:
        print("   [ERROR] PROBLEM: Quant will see NO data!")
    else:
        print(f"   [OK] Sample metadata: {financial_data[0].get('metadata')}")
        print(f"   [OK] Content length: {len(financial_data[0].get('content', ''))} chars")

    # Macro Agent Filter
    macro_data = [c for c in global_context if c.get("metadata", {}).get("type") == "macro"]
    print(f"   Macro Agent would receive: {len(macro_data)} macro items")
    if not macro_data:
        print("   [ERROR] PROBLEM: Macro will see NO data!")
    else:
        print(f"   [OK] Sample metadata: {macro_data[0].get('metadata')}")

    # Step 6: Test Actual Agent Invocation
    print("\n[STEP 6] Testing actual agent invocation...")
    try:
        from app.agents.quant import quant_agent
        result = quant_agent.run(global_context)

        if "Fallback" in result.get("analysis", ""):
            print(f"   [ERROR] Quant Agent used FALLBACK (no data received)")
            print(f"   Analysis: {result.get('analysis')[:200]}...")
        else:
            print(f"   [OK] Quant Agent ran successfully")
            print(f"   Score: {result.get('score')}")
            print(f"   Confidence: {result.get('confidence')}")
    except Exception as e:
        print(f"   [ERROR] Agent invocation failed: {e}")

    print("\n" + "=" * 80)
    print("DEBUG COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    # Test with a known working stock
    import sys
    asset_id = sys.argv[1] if len(sys.argv) > 1 else "RELIANCE.NS"
    debug_data_flow(asset_id)
