from yahooquery import Ticker
import json

t = Ticker('EURUSD=X')
modules = t.get_modules(['summaryDetail', 'financialData', 'price', 'quoteType'])

print(json.dumps(modules, indent=2))
