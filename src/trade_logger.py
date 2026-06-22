import csv
import os
from datetime import datetime

FILE = "data/trade_log.csv"


def log_trade(account_balance, risk, position, rr, pnl, asset):
    file_exists = os.path.isfile(FILE)

    with open(FILE, mode="a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "time",
                "asset",
                "account_balance",
                "risk",
                "position",
                "risk_reward",
                "pnl"
            ])

        writer.writerow([
            datetime.now(),
            asset,
            account_balance,
            risk,
            position,
            rr,
            pnl
        ])