import numpy as np
import pandas as pd


def simple_backtest(spread, zscore_series, entry=2, exit=0.5):
    """
    Proper stat arb backtest:
    - no lookahead bias
    - aligned series
    - normalized returns
    """

    spread, zscore_series = spread.align(zscore_series, join="inner")

    spread = spread.dropna()
    zscore_series = zscore_series.dropna()

    position = 0
    positions = []
    pnl = []

    for i in range(len(spread)):

        z = zscore_series.iloc[i]

        # -------------------------
        # POSITION DECISION
        # -------------------------
        if z > entry:
            position = -1
        elif z < -entry:
            position = 1
        elif abs(z) < exit:
            position = 0

        # store position FIRST (prevents bias)
        positions.append(position)

        # -------------------------
        # RETURN CALC
        # -------------------------
        if i == 0:
            pnl.append(0)
        else:
            ret = (spread.iloc[i] - spread.iloc[i - 1]) / (abs(spread.iloc[i - 1]) + 1e-9)
            pnl.append(position * ret)

    equity = np.cumsum(pnl)

    return pd.DataFrame({
        "spread": spread.values,
        "zscore": zscore_series.values,
        "position": positions,
        "pnl": pnl,
        "equity": equity
    })