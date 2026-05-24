import yfinance as yf
import requests
import json

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
})

try:
    ticker = yf.Ticker('AAPL', session=session)
    info = ticker.info
    print("SUCCESS: Got info.")
    print("Market Cap:", info.get('marketCap'))
    print("Sector:", info.get('sector'))
except Exception as e:
    print("ERROR:", e)
