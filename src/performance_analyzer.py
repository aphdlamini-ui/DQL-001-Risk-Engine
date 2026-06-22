import pandas as pd

FILE = "data/trade_log.csv"


def load_trades():
    try:
        return pd.read_csv(FILE)
    except FileNotFoundError:
        return None


def equity_curve(df):
    equity = [df["account_balance"].iloc[0]]

    for pnl in df["pnl"]:
        equity.append(equity[-1] + pnl)

    return pd.Series(equity[1:])

def drawdown(df):
    equity = equity_curve(df)
    peak = []
    current_peak = 0

    for e in equity:
        current_peak = max(current_peak, e)
        peak.append(current_peak)

    return [e - p for e, p in zip(equity, peak)]


def win_rate(df):
    wins = df[df["pnl"] > 0].shape[0]
    total = df.shape[0]
    return (wins / total) * 100 if total > 0 else 0


def total_pnl(df):
    return df["pnl"].sum()


def pnl_by_asset(df):
    return df.groupby("asset")["pnl"].sum()