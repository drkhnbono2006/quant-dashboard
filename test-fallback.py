import yfinance as yf
print("Trying AAPL Fast Info")
tick = yf.Ticker("AAPL")
try:
    fi = tick.get_fast_info()
    print("Market cap:", fi.get('marketCap') or fi.get('market_cap'))
except Exception as e:
    print("Error:", e)
