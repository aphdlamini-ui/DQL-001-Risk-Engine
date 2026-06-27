import csv
import os
from datetime import datetime

FILE = "data/trade_log.csv"


def log_trade(
    account_balance,
    risk,
    position,
    rr,
    pnl,
    asset,
    signal=None,
    zscore=None,
    strategy="stat_arb"
):

    file_exists = os.path.isfile(FILE)

    with open(FILE, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "time",
                "asset",
                "strategy",
                "signal",
                "zscore",
                "account_balance",
                "risk",
                "position",
                "risk_reward",
                "pnl"
            ])

        writer.writerow([
            datetime.now(),
            asset,
            strategy,
            signal,
            zscore,
            account_balance,
            risk,
            position,
            rr,
            pnl
        ])