import sys
import os
from dotenv import load_dotenv

# Ensure backend directory is in path
sys.path.append(os.getcwd())

# Force reload of env vars
load_dotenv(override=True)

from app.services.fred_service import fred_service

print("🔎 Verifying FRED API Key Integration (Including INDIA)...")
print(f"Key Present: {'Yes' if fred_service.api_key else 'No'}")

try:
    print("📡 Fetching Macro Data...")
    fred_service._cache = {} # Clear cache
    
    data = fred_service.get_macro_summary()
    api_source = data.get("source", "Unknown")
    
    print(f"Source: {api_source}")
    
    if "Mock" in api_source:
        print("❌ Using Mock Data.")
    elif "FRED API" in api_source:
        print("✅ SUCCESS! Using Live FRED API.")
        
        inds = data.get("indicators", {})
        print(f"Total Indicators: {len(inds)}")
        
        # Check US Data
        if "inflation" in inds:
            inf = inds["inflation"]
            print(f"🇺🇸 US Inflation: {inf.get('value')} ({inf.get('date')})")
            
        # Check India Data
        india_keys = [k for k in inds.keys() if "india" in k]
        print(f"🇮🇳 India Indicators Found: {len(india_keys)}")
        
        if not india_keys:
            print("❌ No India data found!")
        else:
            for k in india_keys:
                 val = inds[k].get("value")
                 date = inds[k].get("date")
                 title = inds[k].get("description")
                 print(f"  - {title}: {val} ({date})")
            
    else:
        print(f"⚠️ Unexpected Source: {api_source}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
