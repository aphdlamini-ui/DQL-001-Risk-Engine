import yfinance as yf
import numpy as np
import pandas as pd
from quant_stats import (
    volatility,
    rolling_correlation,
    sharpe_ratio,
    cointegration_test,
    zscore
)

# =========================================================
# SIGNAL SCORING ENGINE
# =========================================================
def signal_score(vol, corr, sharpe, coint_p, zscore_val):
    score = 100

    # volatility penalty
    if vol > 0.05:
        score -= 25

    # correlation penalty
    if corr < 0.6:
        score -= 25

    # sharpe penalty
    if sharpe < 0:
        score -= 20

    # cointegration penalty
    if coint_p > 0.05:
        score -= 30

    # z-score strength bonus
    score += min(abs(zscore_val) * 10, 20)

    return max(0, min(100, score))


# =========================================================
# DATA LAYER
# =========================================================
def get_price(symbol):
    data = yf.download(symbol, period="5d", interval="1h", progress=False)

    if data is None or data.empty:
        return None

    return data["Close"].dropna().astype(float)


# =========================================================
# 1. BTC / ETH PAIR TRADE ENGINE
# =========================================================
def btc_eth_signal():
    btc = get_price("BTC-USD")
    eth = get_price("ETH-USD")

    if btc is None or eth is None:
        return 0, "No data", 0

    btc, eth = btc.align(eth, join="inner")

    if len(btc) < 30:
        return 0, "Insufficient data", 0

    spread = btc - eth

    # cointegration filter (ONLY ONCE)
    coint_p = cointegration_test(btc, eth)

    if coint_p > 0.05:
        return 0, "SKIP: No cointegration", 0

    # features
    vol = volatility(spread)

    corr_series = rolling_correlation(btc, eth)
    corr = corr_series.dropna().iloc[-1] if len(corr_series.dropna()) > 0 else 0

    sharpe = sharpe_ratio(spread)
    z_series = zscore(spread)
    z = float(z_series.iloc[-1]) if len(z_series) > 0 else 0

    # score
    score = signal_score(vol, corr, sharpe, coint_p, z)

    # filter
    if score < 50:
        return z, "NO TRADE (low quality)", score

    # trading logic
    if z > 2:
        signal = "SELL BTC / BUY ETH"
    elif z < -2:
        signal = "BUY BTC / SELL ETH"
    else:
        signal = "HOLD"

    return z, signal, score


# =========================================================
# 2. SINGLE ASSET MEAN REVERSION ENGINE
# =========================================================
def single_asset_signal(symbol, name):
    data = get_price(symbol)

    if data is None or len(data) < 10:
        return 0, "No data", 0

    z_series = zscore(data).dropna()

    if len(z_series) == 0:
        return 0, "No data", 0

    latest = z_series.iloc[-1]

    # FORCE scalar if needed
    latest = float(np.asarray(latest).flatten()[0])

    if latest > 2:
        signal = f"{name} overbought → SHORT"
    elif latest < -2:
        signal = f"{name} oversold → LONG"
    else:
        signal = f"{name} neutral"

    # simple scoring model (can upgrade in Sprint 2.6)
    score = max(0, 100 - abs(latest) * 20)

    return latest, signal, score


# =========================================================
# 3. ORCHESTRATION LAYER
# =========================================================
def run_all():
    btc_z, btc_signal, btc_score = btc_eth_signal()

    gold_z, gold_signal, gold_score = single_asset_signal("GC=F", "Gold")
    nas_z, nas_signal, nas_score = single_asset_signal("^IXIC", "NASDAQ")

    return {
        "btc_z": btc_z,
        "btc_signal": btc_signal,
        "btc_score": btc_score,

        "gold_z": gold_z,
        "gold_signal": gold_signal,
        "gold_score": gold_score,

        "nas_z": nas_z,
        "nas_signal": nas_signal,
        "nas_score": nas_score
    }