import sys, os
sys.path.append(os.getcwd())
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

from app.agents.scout import ScoutAgent
import traceback

print("Testing _get_financials_deep_static for EURUSD=X...")
try:
    data = ScoutAgent._get_financials_deep_static('EURUSD=X')
    print("Success!")
    print(data)
except Exception:
    traceback.print_exc()
