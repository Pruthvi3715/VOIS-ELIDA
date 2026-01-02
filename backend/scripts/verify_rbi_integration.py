import sys
import os

# Ensure backend directory is in path
sys.path.append(os.getcwd())

from app.services.rbi_service import rbi_service
from app.agents.scout import ScoutAgent

def verify_rbi():
    print("🔎 Step 1: Testing RBIService Scraper...")
    rbi_results = rbi_service.get_real_time_rates()
    print(f"Scraper Output: {rbi_results}")
    
    if "repo_rate" in rbi_results:
        print(f"✅ Scraper Success: Repo Rate = {rbi_results['repo_rate']}%")
    else:
        print(f"❌ Scraper Failed: {rbi_results.get('error')}")

    print("\n🔎 Step 2: Testing ScoutAgent integration...")
    scout = ScoutAgent()
    macro_data = scout._get_macro_data_static()
    
    repo_val = macro_data.get("fred_india_repo_rate")
    repo_desc = macro_data.get("fred_india_repo_rate_desc")
    
    print(f"Scout Macro Data - Repo Rate: {repo_val}")
    print(f"Scout Macro Data - Description: {repo_desc}")
    
    if repo_desc == "Policy Repo Rate (RBI Live)":
        print("✅ Scout Integration Success: Live RBI data is being used!")
    else:
        print("⚠️ Scout Integration Warning: Falling back to FRED/Mock data.")

if __name__ == "__main__":
    verify_rbi()
