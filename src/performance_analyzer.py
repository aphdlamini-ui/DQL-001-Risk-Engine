import pandas as pd

FILE = "data/trade_log.csv"


def load_trades():
    try:
        return pd.read_csv(FILE)
    except FileNotFoundError:
        return None


# -----------------------------
# EQUITY CURVE (FIXED)
# -----------------------------
def equity_curve(df):
    df = df.copy()

    df["equity"] = df["account_balance"] + df["pnl"].cumsum()

    return df["equity"]


# -----------------------------
# DRAWDOWN (FIXED)
# -----------------------------
def drawdown(df):
    equity = equity_curve(df)

    peak = equity.cummax()
    dd = equity - peak

    return dd


# -----------------------------
# WIN RATE
# -----------------------------
def win_rate(df):
    return (df["pnl"] > 0).mean() * 100 if len(df) > 0 else 0


# -----------------------------
# TOTAL PNL
# -----------------------------
def total_pnl(df):
    return df["pnl"].sum()


# -----------------------------
# PNL BY ASSET
# -----------------------------
def pnl_by_asset(df):
    return df.groupby("asset")["pnl"].sum()