import sys, os
sys.path.append(os.getcwd())
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

from app.agents.scout import scout_agent

print("Fetching Bitcoin (BTC) data...")
try:
    # Test Bitcoin
    data = scout_agent.collect_data('BTC')
    financials = data.get('financials', {})
    technicals = data.get('technicals', {})

    print('='*60)
    print('BITCOIN (BTC) - CRYPTO DATA TEST')
    print('='*60)
    print(f"Source: {financials.get('source', 'N/A')}")
    print(f"Name: {financials.get('company_name', 'N/A')}")
    print(f"Price: ${financials.get('current_price', 'N/A')}")
    print(f"Market Cap: {financials.get('market_cap', 'N/A')}")
    print(f"24h Change: {financials.get('price_change_24h', 'N/A')}%")
    print(f"ATH: ${financials.get('52_week_high', 'N/A')}")
    print(f"ATL: ${financials.get('52_week_low', 'N/A')}")
    print(f"Sector: {financials.get('sector', 'N/A')}")
    
    rsi = technicals.get('rsi_14', 'N/A')
    print(f"RSI: {rsi}")
    print(f"Trend: {technicals.get('trend_signal', 'N/A')}")
    print(f"History Points: {len(technicals.get('history', []))}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
