import yfinance as yf


# -----------------------------
# HISTORICAL PRICES (FOR STRATS)
# -----------------------------
def get_price_series(symbol, period="5d", interval="1h"):
    data = yf.download(symbol, period=period, interval=interval, progress=False)

    if data is None or data.empty:
        return None

    return data["Close"].dropna().astype(float)


# -----------------------------
# SAFE SNAPSHOT ENGINE (FOR UI)
# -----------------------------
def get_market_summary(ticker):
    try:
        data = yf.Ticker(ticker)
        info = data.fast_info

        price = info.get("lastPrice")
        high = info.get("dayHigh")
        low = info.get("dayLow")
        change = info.get("regularMarketChangePercent")

        return {
            "price": float(price) if price is not None else None,
            "high": float(high) if high is not None else None,
            "low": float(low) if low is not None else None,
            "change": float(change) if change is not None else None
        }

    except Exception:
        return {
            "price": None,
            "high": None,
            "low": None,
            "change": None
        }