from risk_calculator import (
    calculate_risk,
    calculate_position_size,
    calculate_risk_reward,
    portfolio_exposure
)

from trade_logger import log_trade
from performance_analyzer import load_trades, total_pnl


# -----------------------------
# ACCOUNT SETUP
# -----------------------------
account_balance = 2000
risk_percent = 1

risk_amount = calculate_risk(account_balance, risk_percent)

print("Risk per trade:", risk_amount)


# -----------------------------
# POSITION SIZING
# -----------------------------
position = calculate_position_size(
    risk_amount=risk_amount,
    stop_loss_pips=50,
    pip_value=1
)

print("Position size:", position)


# -----------------------------
# RISK REWARD
# -----------------------------
rr = calculate_risk_reward(
    entry=100,
    stop_loss=95,
    take_profit=120
)

print("Risk:Reward:", rr)


# -----------------------------
# LOG SAMPLE TRADE (NOW CONNECTED)
# -----------------------------
log_trade(
    account_balance=account_balance,
    risk=risk_amount,
    position=position,
    rr=rr,
    pnl=25,   # simulated
    asset="BTC-ETH",
    signal="stat_arb_test",
    zscore=2.1
)


# -----------------------------
# ANALYTICS
# -----------------------------
df = load_trades()

if df is not None:
    print("Total PnL:", total_pnl(df))