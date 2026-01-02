import sys, os
sys.path.append(os.getcwd())
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

from app.agents.scout import scout_agent

print("Fetching Forex (EURUSD=X) data...")
try:
    # Test Forex
    data = scout_agent.collect_data('EURUSD=X')
    financials = data.get('financials', {})
    technicals = data.get('technicals', {})

    print('='*60)
    print('EUR/USD - FOREX DATA TEST')
    print('='*60)
    print(f"Source: {financials.get('source', 'N/A')}")
    print(f"Name: {financials.get('company_name', 'N/A')}")
    print(f"Price: {financials.get('current_price', 'N/A')}")
    print(f"Sector: {financials.get('sector', 'N/A')}")
    print(f"Industry: {financials.get('industry', 'N/A')}")
    
    rsi = technicals.get('rsi_14', 'N/A')
    print(f"RSI: {rsi}")
    print(f"Trend: {technicals.get('trend_signal', 'N/A')}")
    print(f"History Points: {len(technicals.get('history', []))}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
