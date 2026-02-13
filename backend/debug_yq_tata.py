from yahooquery import Ticker
import json

ticker_name = "TATAMOTORS.NS"
print(f"Fetching modules for {ticker_name}...")
t = Ticker(ticker_name)

try:
    modules = t.get_modules(['summaryDetail', 'financialData', 'defaultKeyStatistics', 'summaryProfile', 'price', 'quoteType'])
    print("Modules keys:", modules.keys())
    if ticker_name in modules:
        print(f"Type of value for {ticker_name}:", type(modules[ticker_name]))
        if isinstance(modules[ticker_name], dict):
             print("Keys in ticker data:", modules[ticker_name].keys())
        else:
             print("Value content:", modules[ticker_name])
    else:
        print(f"{ticker_name} NOT in modules. Full modules content:")
        print(json.dumps(modules, indent=2, default=str))
except Exception as e:
    print("Exception:", e)
