"""
Test YahooQuery Data Fetching for ITC.NS
Verifies that the Scout Agent can properly pull live data.
"""
import json
import sys
from datetime import datetime

sys.path.insert(0, '.')

print("=" * 70)
print("YAHOOQUERY DATA FETCH TEST - ITC.NS")
print(f"Timestamp: {datetime.now().isoformat()}")
print("=" * 70)

# Test 1: Direct YahooQuery Test
print("\n[TEST 1] Direct YahooQuery Connection")
print("-" * 50)

try:
    from yahooquery import Ticker
    
    ticker = Ticker("ITC.NS")
    
    # Fetch modules
    print("Fetching summary data...")
    modules = ticker.get_modules(['summaryDetail', 'financialData', 'defaultKeyStatistics', 'summaryProfile'])
    
    if "ITC.NS" in modules:
        data = modules["ITC.NS"]
        print(f"✅ Data received for ITC.NS")
        print(f"   Modules: {list(data.keys())}")
    else:
        print(f"❌ ITC.NS not in response. Keys: {list(modules.keys())}")
        data = None
        
except Exception as e:
    print(f"❌ YahooQuery Error: {e}")
    data = None

# Test 2: Scout Agent Test
print("\n[TEST 2] Scout Agent Data Collection")
print("-" * 50)

try:
    from app.agents.scout import scout_agent
    
    scout_data = scout_agent.collect_data("ITC.NS")
    
    print(f"✅ Scout Agent collected data successfully")
    print(f"   Collection Timestamp: {scout_data.get('collection_timestamp')}")
    print(f"   Data Quality: {scout_data.get('data_quality', {}).get('overall', 'Unknown')}")
    
    # Check each component
    components = ['financials', 'technicals', 'macro', 'news']
    for comp in components:
        comp_data = scout_data.get(comp, {})
        source = comp_data.get('source', 'N/A') if isinstance(comp_data, dict) else 'List'
        print(f"   - {comp}: {source}")
        
except Exception as e:
    print(f"❌ Scout Agent Error: {e}")
    import traceback
    traceback.print_exc()
    scout_data = None

# Test 3: Detailed Data Inspection
print("\n[TEST 3] Detailed Data Inspection")
print("-" * 50)

if scout_data:
    # Financials
    fin = scout_data.get('financials', {})
    print("\n📊 FINANCIALS:")
    print(f"   Symbol: {fin.get('symbol')}")
    print(f"   Source: {fin.get('source')}")
    print(f"   Current Price: {fin.get('current_price')} {fin.get('currency', '')}")
    print(f"   P/E Ratio: {fin.get('pe_ratio')}")
    print(f"   Forward P/E: {fin.get('forward_pe')}")
    print(f"   PEG Ratio: {fin.get('peg_ratio')}")
    print(f"   Market Cap: {fin.get('market_cap')}")
    print(f"   Profit Margins: {fin.get('profit_margins')}")
    print(f"   ROE: {fin.get('return_on_equity')}")
    print(f"   Debt/Equity: {fin.get('debt_to_equity')}")
    print(f"   Sector: {fin.get('sector')}")
    print(f"   Industry: {fin.get('industry')}")
    
    # Technicals
    tech = scout_data.get('technicals', {})
    print("\n📈 TECHNICALS:")
    print(f"   Source: {tech.get('source')}")
    print(f"   Current Price: {tech.get('current_price')}")
    print(f"   SMA 50: {tech.get('sma_50')}")
    print(f"   SMA 200: {tech.get('sma_200')}")
    print(f"   Trend: {tech.get('trend_signal')}")
    print(f"   RSI (14): {tech.get('rsi_14')} ({tech.get('rsi_status')})")
    print(f"   Volatility: {tech.get('volatility_annualized')}")
    print(f"   52W High: {tech.get('high_52w')}")
    print(f"   52W Low: {tech.get('low_52w')}")
    print(f"   % From 52W High: {tech.get('pct_from_52w_high')}%")
    print(f"   Data Points: {tech.get('data_points')}")
    
    # Macro
    macro = scout_data.get('macro', {})
    print("\n🌍 MACRO:")
    print(f"   Source: {macro.get('source')}")
    print(f"   VIX: {macro.get('volatility_index')} ({macro.get('vix_interpretation', 'N/A')})")
    print(f"   10Y Yield: {macro.get('interest_rate_proxy')}")
    print(f"   Market Index: {macro.get('market_index')}")
    
    # News
    news = scout_data.get('news', [])
    print("\n📰 NEWS:")
    if isinstance(news, list):
        for i, item in enumerate(news[:5], 1):
            if isinstance(item, dict):
                title = item.get('title', 'No title')[:60]
                source = item.get('source', 'Unknown')
                publisher = item.get('publisher', '')
                print(f"   {i}. [{source}] {title}...")
                if publisher:
                    print(f"      Publisher: {publisher}")
            else:
                print(f"   {i}. {str(item)[:70]}...")
    
    # Data Quality
    quality = scout_data.get('data_quality', {})
    print("\n✅ DATA QUALITY:")
    print(f"   Overall: {quality.get('overall')}")
    print(f"   Components: {quality.get('components')}")
    if quality.get('issues'):
        print(f"   Issues: {quality.get('issues')}")

# Save results to file
print("\n" + "=" * 70)
print("SAVING RESULTS TO FILE")
print("=" * 70)

output = {
    "test_timestamp": datetime.now().isoformat(),
    "symbol": "ITC.NS",
    "yahooquery_direct_test": "Success" if data else "Failed",
    "scout_agent_test": "Success" if scout_data else "Failed",
    "data": scout_data
}

output_file = "itc_data_test_results.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, default=str)

print(f"✅ Results saved to: {output_file}")

# Final Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

if scout_data:
    fin = scout_data.get('financials', {})
    is_live = "Live" in str(fin.get('source', '')) and "Mock" not in str(fin.get('source', ''))
    
    if is_live:
        print("✅ YahooQuery is pulling LIVE data successfully!")
        print(f"   Stock: ITC.NS")
        print(f"   Price: ₹{fin.get('current_price')}")
        print(f"   Sector: {fin.get('sector')}")
    else:
        print("⚠️ YahooQuery returned MOCK/FALLBACK data")
        print("   This could be due to API rate limits or network issues")
else:
    print("❌ Failed to fetch data")
