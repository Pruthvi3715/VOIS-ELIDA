import sys
import os
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.orchestrator import orchestrator
from app.models.investor_dna import DEFAULT_INVESTOR_DNA

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_with_provider.py <provider> <output_file> [asset_id]")
        print("Example: python run_with_provider.py gemini output.json IDEA.NS")
        sys.exit(1)
        
    provider = sys.argv[1]
    output_file = sys.argv[2]
    asset_id = sys.argv[3] if len(sys.argv) > 3 else "IDEA.NS"
    
    print(f"============================================================")
    print(f"RUNNING ANALYSIS WITH: {provider.upper()}")
    print(f"============================================================")
    
    start_time = time.time()
    
    try:
        # 1. Ingest Data (Scout + PDF RAG)
        print(f"Ingesting {asset_id}...")
        orchestrator.ingest_asset(asset_id)
        
        # 2. Run Analysis (Orchestrator -> Retrieval -> Grading -> Agents)
        print(f"Analyzing {asset_id}...")
        result = orchestrator.retrieve_context(
            query=f"Financial analysis of {asset_id}",
            asset_id=asset_id,
            investor_dna=DEFAULT_INVESTOR_DNA
        )
        
        # 3. Save Output
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
            
        elapsed = time.time() - start_time
        print(f"\n✅ COMPLETED in {elapsed:.1f}s")
        print(f"Provider: {provider}")
        print(f"Match Score: {result.get('match_score')}")
        print(f"Recommendation: {result.get('match_result', {}).get('recommendation')}")
        print(f"Output saved to: {output_file}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
