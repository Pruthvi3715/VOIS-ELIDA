import requests
import sys

try:
    res = requests.post("http://localhost:8000/api/portfolio/scan", json={"user_id": "test", "tickers": ["AAPL"]})
    print(f"Status: {res.status_code}")
    print(res.text)
except Exception as e:
    print(e)
