import yfinance as yf
print("Downloading AAPL...", flush=True)
try:
    ticker = yf.Ticker("AAPL")
    hist = ticker.history(period="1d")
    print(hist)
    print("Done", flush=True)
except Exception as e:
    print(e)
