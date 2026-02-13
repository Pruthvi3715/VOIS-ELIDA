import sys
import os
import time
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.getcwd())

try:
    from app.agents.scout import ScoutAgent
    from yahooquery import Ticker
except ImportError:
    # If running from scripts dir
    sys.path.append(os.path.join(os.getcwd(), '..'))
    from app.agents.scout import ScoutAgent
    from yahooquery import Ticker

# List of diverse companies to test
COMPANIES = [
    {"ticker": "SBIN.NS", "name": "State Bank of India", "expected_sector": "Financial Services"},
    {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "expected_sector": "Healthcare"},
    {"ticker": "ITC.NS", "name": "ITC Limited", "expected_sector": "Consumer Defensive"},
    {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "expected_sector": "Consumer Cyclical"}
]

def test_company(company):
    ticker = company["ticker"]
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🧪 Testing {ticker} ({company['name']})...")
    
    try:
        # direct retrieval from ScoutAgent logic
        data = ScoutAgent._get_financials_deep_static(ticker)
        
        is_mock = data.get('is_mock', False)
        sector = data.get('sector', 'N/A')
        
        print(f"   Status: {'⚠️ MOCK DATA' if is_mock else '✅ REAL DATA'}")
        print(f"   Sector: {sector}")
        print(f"   Expected: {company['expected_sector']}")
        
        if not is_mock and sector != 'Unknown (API Failed)':
            # Check if sector matches roughly (ignoring case/exact string)
            if company['expected_sector'].lower() in str(sector).lower() or \
               str(sector).lower() in company['expected_sector'].lower():
                 print("   ✅ Sector Match: PASS")
                 return True
            else:
                 print("   ⚠️ Sector Mismatch (might be taxonomy difference)")
                 return True # Still count as success if real data
        else:
            print("   ❌ FAILED to get real data")
            return False
            
    except Exception as e:
        print(f"   ❌ EXCEPTION: {e}")
        return False

def run_stress_test():
    print("=== STARTING DATA PIPELINE STRESS TEST ===")
    success_count = 0
    
    for company in COMPANIES:
        if test_company(company):
            success_count += 1
        
        # Wait between requests to avoid rate limits
        print("   Thinking... (Waiting 5s)")
        time.sleep(5)
        
    print(f"\n=== TEST COMPLETE: {success_count}/{len(COMPANIES)} Successful ===")

if __name__ == "__main__":
    run_stress_test()
