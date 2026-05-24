import yfinance as yf

try:
    ticker = yf.Ticker('AAPL')
    info = ticker.info
    print("SUCCESS: Got info.")
    print("Keys found:", len(info.keys()))
    print("Market Cap:", info.get('marketCap'))
    print("Sector:", info.get('sector'))
except Exception as e:
    print("ERROR:", e)
