import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
import time

print("Starting import test...", flush=True)
start = time.time()
try:
    from app.orchestrator import orchestrator
    print(f"Import done in {time.time() - start:.2f}s", flush=True)
except Exception as e:
    print(f"Import failed: {e}")
