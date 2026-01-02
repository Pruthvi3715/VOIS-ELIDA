import sys
import os
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.getcwd())
load_dotenv(override=True)

print("Attempting to import FinancialOrchestrator...")
try:
    from app.orchestrator import orchestrator
    print("✅ Orchestrator imported successfully.")
except Exception as e:
    print(f"❌ Import failed! Error: {e}")
    import traceback
    traceback.print_exc()
