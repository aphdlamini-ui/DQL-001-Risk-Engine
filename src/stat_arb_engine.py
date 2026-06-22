import numpy as np
import yfinance as yf


def get_price(symbol):
    data = yf.download(symbol, period="5d", interval="1h")
    return data["Close"].dropna().squeeze()


def zscore(series):
    return (series - series.mean()) / series.std()


# --- BTC vs ETH TRUE PAIR TRADE ---
def btc_eth_signal():
    btc = get_price("BTC-USD").squeeze()
    eth = get_price("ETH-USD").squeeze()

    btc, eth = btc.align(eth, join="inner")
    btc = btc.squeeze()
    eth = eth.squeeze()

    spread = (btc - eth).dropna()
    z = zscore(spread).dropna().astype(float)

    latest = z.iloc[-1].item()

    if latest > 2:
        signal = "BTC overvalued vs ETH → SELL BTC / BUY ETH"
    elif latest < -2:
        signal = "BTC undervalued vs ETH → BUY BTC / SELL ETH"
    else:
        signal = "BTC/ETH neutral"

    return latest, signal


# --- SINGLE ASSET MEAN REVERSION ---
def single_asset_signal(symbol, name):
    data = get_price(symbol)

    # FORCE 1D CLEAN SERIES
    data = data.dropna().astype(float)

    z = zscore(data).dropna()

    latest = float(z.iloc[-1])   # FORCE SCALAR

    if latest > 2:
        signal = f"{name} overbought → potential SHORT"
    elif latest < -2:
        signal = f"{name} oversold → potential LONG"
    else:
        signal = f"{name} neutral"

    return latest, signal


def run_all():
    btc_z, btc_signal = btc_eth_signal()

    gold_z, gold_signal = single_asset_signal("GC=F", "XAUUSD (Gold)")
    nas_z, nas_signal = single_asset_signal("^IXIC", "NASDAQ")

    return {
        "btc_z": btc_z,
        "btc_signal": btc_signal,
        "gold_z": gold_z,
        "gold_signal": gold_signal,
        "nas_z": nas_z,
        "nas_signal": nas_signal
    }