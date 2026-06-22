import yfinance as yf

def get_price(symbol):
    data = yf.download(symbol, period="5d", interval="1h")
    return data["Close"]