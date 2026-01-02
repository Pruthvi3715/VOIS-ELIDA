import sys, os
sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv(override=True)
from app.agents.scout import scout_agent

# Test with Suzlon to compare with Screener.in
data = scout_agent.collect_data('SUZLON.NS')
financials = data.get('financials', {})
technicals = data.get('technicals', {})

print('='*60)
print('SUZLON.NS - ENHANCED DATA (Yahoo + Screener.in)')
print('='*60)

# Basic Info
print('\n📋 BASIC INFO:')
print(f"  Company Name: {financials.get('company_name', 'N/A')}")
print(f"  Sector: {financials.get('sector', 'N/A')}")
print(f"  Industry: {financials.get('industry', 'N/A')}")

# Price Data
print('\n💰 PRICE DATA:')
print(f"  Current Price: ₹{financials.get('current_price', 'N/A')}")
print(f"  Previous Close: ₹{financials.get('previous_close', 'N/A')}")
print(f"  52W High: ₹{financials.get('52_week_high', 'N/A')}")
print(f"  52W Low: ₹{financials.get('52_week_low', 'N/A')}")
print(f"  Beta: {financials.get('beta', 'N/A')}")

# Valuation
print('\n📊 VALUATION:')
print(f"  Market Cap: {financials.get('market_cap', 'N/A')}")
print(f"  P/E Ratio: {financials.get('pe_ratio', 'N/A')}")
print(f"  Forward P/E: {financials.get('forward_pe', 'N/A')}")
print(f"  PEG Ratio: {financials.get('peg_ratio', 'N/A')}")
print(f"  Price/Book: {financials.get('price_to_book', 'N/A')}")
print(f"  Book Value: {financials.get('book_value', 'N/A')}")
print(f"  Face Value: ₹{financials.get('face_value', 'N/A')}")

# Profitability (includes ROCE from Screener)
print('\n📈 PROFITABILITY:')
print(f"  ROE: {financials.get('return_on_equity', 'N/A')}")
print(f"  ROCE: {financials.get('roce', 'N/A')} (from Screener.in)")
print(f"  Profit Margins: {financials.get('profit_margins', 'N/A')}")

# Dividend
print('\n💵 DIVIDEND:')
print(f"  Dividend Yield: {financials.get('dividend_yield', 'N/A')}")
print(f"  Dividend Rate: {financials.get('dividend_rate', 'N/A')}")

# Shareholding (from Screener.in)
print('\n👥 SHAREHOLDING (from Screener.in):')
print(f"  Promoter: {financials.get('promoter_holding', 'N/A')}%")
print(f"  FII: {financials.get('fii_holding', 'N/A')}%")
print(f"  DII: {financials.get('dii_holding', 'N/A')}%")

# Growth (from Screener.in)
print('\n📊 GROWTH (from Screener.in):')
print(f"  Revenue Growth: {financials.get('revenue_growth', 'N/A')}")
print(f"  Earnings Growth: {financials.get('earnings_growth', 'N/A')}")
print(f"  Sales Growth (5yr): {financials.get('sales_growth_5yr', 'N/A')}")
print(f"  Profit Growth (5yr): {financials.get('profit_growth_5yr', 'N/A')}")

# Financial Health
print('\n🏦 FINANCIAL HEALTH:')
print(f"  Debt/Equity: {financials.get('debt_to_equity', 'N/A')}")
print(f"  Current Ratio: {financials.get('current_ratio', 'N/A')}")

# Technicals
print('\n📉 TECHNICALS:')
print(f"  RSI: {technicals.get('rsi_14', 'N/A')}")
print(f"  Trend: {technicals.get('trend_signal', 'N/A')}")

print('\n' + '='*60)
print('COMPARISON WITH SCREENER.IN:')
print('='*60)
print(f"  P/E:     VOIS={financials.get('pe_ratio', 'N/A')} | Screener=22.5")
print(f"  ROE:     VOIS={financials.get('return_on_equity', 'N/A')} | Screener=41.4%")
print(f"  ROCE:    VOIS={financials.get('roce', 'N/A')} | Screener=32.5%")
print(f"  52W H:   VOIS=₹{financials.get('52_week_high', 'N/A')} | Screener=₹74.3")
print(f"  52W L:   VOIS=₹{financials.get('52_week_low', 'N/A')} | Screener=₹46.0")
