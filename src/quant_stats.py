import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint


# =========================================================
# SAFE CLEANING HELPER (CRITICAL)
# =========================================================
def _clean(series):
    if series is None:
        return None

    series = series.copy()
    series = series.replace([np.inf, -np.inf], np.nan).dropna()

    if len(series) == 0:
        return None

    return series.astype(float)


# =========================================================
# VOLATILITY (ROBUST)
# =========================================================
def volatility(series):
    series = _clean(series)
    if series is None or len(series) < 2:
        return 0.0

    returns = series.pct_change().dropna()
    if len(returns) == 0:
        return 0.0

    return float(np.std(returns) * np.sqrt(len(returns)))


# =========================================================
# ROLLING CORRELATION (SAFE)
# =========================================================
def rolling_correlation(x, y, window=20):
    x = _clean(x)
    y = _clean(y)

    if x is None or y is None:
        return pd.Series(dtype=float)

    x, y = x.align(y, join="inner")

    if len(x) < window:
        return pd.Series(dtype=float)

    return x.rolling(window).corr(y)


# =========================================================
# SHARPE RATIO (ROBUST)
# =========================================================
def sharpe_ratio(series, risk_free=0):
    series = _clean(series)
    if series is None:
        return 0.0

    returns = series.pct_change().dropna()
    if len(returns) == 0:
        return 0.0

    excess = returns - risk_free
    std = np.std(excess)

    if std == 0:
        return 0.0

    return float(np.mean(excess) / std)


# =========================================================
# SKEWNESS
# =========================================================
def skewness(series):
    series = _clean(series)
    if series is None or len(series) < 3:
        return 0.0

    returns = series.pct_change().dropna()
    if len(returns) < 3:
        return 0.0

    return float(returns.skew())


# =========================================================
# KURTOSIS
# =========================================================
def kurtosis(series):
    series = _clean(series)
    if series is None or len(series) < 4:
        return 0.0

    returns = series.pct_change().dropna()
    if len(returns) < 4:
        return 0.0

    return float(returns.kurtosis())


# =========================================================
# Z-SCORE (SAFE)
# =========================================================
def zscore(series):
    if series is None:
        return pd.Series(dtype=float)

    series = series.dropna()

    if len(series) < 2:
        return pd.Series(dtype=float)

    mean = series.mean()
    std = series.std()

    # FORCE SCALAR SAFETY (IMPORTANT FIX)
    if isinstance(std, pd.Series):
        std = std.iloc[0]

    std = float(std)

    if std == 0:
        return pd.Series([0] * len(series), index=series.index)

    return (series - mean) / std


# =========================================================
# VOLATILITY REGIME
# =========================================================
def volatility_regime(series, threshold=0.02):
    series = _clean(series)
    if series is None:
        return "UNKNOWN"

    returns = series.pct_change().dropna()
    if len(returns) == 0:
        return "UNKNOWN"

    vol = np.std(returns)

    return "HIGH_VOL" if vol > threshold else "LOW_VOL"


# =========================================================
# COINTEGRATION TEST (FULLY SAFE)
# =========================================================
def cointegration_test(series1, series2):
    try:
        s1 = _clean(series1)
        s2 = _clean(series2)

        if s1 is None or s2 is None:
            return 1.0

        # align
        s1, s2 = s1.align(s2, join="inner")

        # remove extra noise again after alignment
        s1 = _clean(s1)
        s2 = _clean(s2)

        if s1 is None or s2 is None:
            return 1.0

        # minimum data requirement (VERY IMPORTANT)
        if len(s1) < 30 or len(s2) < 30:
            return 1.0

        score, p_value, _ = coint(s1, s2)

        return float(p_value)

    except Exception:
        return 1.0