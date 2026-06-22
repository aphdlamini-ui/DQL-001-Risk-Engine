import streamlit as st
from trade_logger import log_trade
from performance_analyzer import pnl_by_asset
from performance_analyzer import (
    load_trades,
    equity_curve,
    drawdown,
    win_rate,
    total_pnl
)
from risk_calculator import (
    calculate_risk,
    calculate_position_size,
    calculate_risk_reward,
    portfolio_exposure
)
from stat_arb_engine import run_all

st.set_page_config(page_title="DQL Risk Engine", layout="centered")

st.title("📊 DQL Risk Engine")

# Inputs
account_balance = st.number_input("Account Balance", value=2000)
risk_percent = st.slider("Risk %", 0.1, 10.0, 1.0)

entry = st.number_input("Entry Price", value=100.0)
stop_loss = st.number_input("Stop Loss", value=95.0)
take_profit = st.number_input("Take Profit", value=120.0)

# THIS is “under sliders”
asset = st.selectbox(
    "Select Asset",
    ["BTCUSD", "ETHUSD", "XAUUSD", "NASDAQ"]
)

st.divider()

# Calculations
risk_amount = calculate_risk(account_balance, risk_percent)

position = calculate_position_size(
    risk_amount=risk_amount,
    stop_loss_pips=abs(entry - stop_loss),
    pip_value=1
)

rr = calculate_risk_reward(entry, stop_loss, take_profit)

# Output
st.subheader("Results")

st.write(f"💰 Risk per Trade: ${risk_amount:.2f}")
st.write(f"📦 Position Size: {position:.4f}")
st.write(f"⚖️ Risk:Reward: {rr:.2f}")

# Fake exposure demo
st.write(f"📉 Portfolio Exposure: {portfolio_exposure([risk_amount, 15, 10])}")

if st.button("📊 Simulate Trade"):

    pnl = risk_amount * rr  # simple model

    log_trade(
        account_balance,
        risk_amount,
        position,
        rr,
        pnl,
        asset
)

    st.success("Trade logged successfully!")
    st.write(f"💰 PnL: ${pnl:.2f}")

st.divider()
st.title("📊 Performance Dashboard")

df = load_trades()

if df is not None and len(df) > 0:

    st.write(df)
    eq = equity_curve(df)
    dd = drawdown(df)

    st.metric("Total PnL", f"${total_pnl(df):.2f}")
    st.metric("Win Rate", f"{win_rate(df):.2f}%")

    st.subheader("📈 Equity Curve")
    st.line_chart(eq, use_container_width=True)

    st.subheader("📉 Drawdown")
    st.line_chart(dd, use_container_width=True)

    st.subheader("📊 PnL by Asset")
    st.bar_chart(pnl_by_asset(df))

else:
    st.info("No trades yet. Click 'Simulate Trade' first.")

    st.divider()
st.title("📡 Multi-Market Stat Arb Engine")

data = run_all()

# BTC vs ETH
st.subheader("₿ Crypto Pair (BTC vs ETH)")
st.metric("Z-Score", f"{data['btc_z']:.2f}")
st.write(data["btc_signal"])

st.divider()

# Gold
st.subheader("🥇 XAUUSD (Gold)")
st.metric("Z-Score", f"{data['gold_z']:.2f}")
st.write(data["gold_signal"])

st.divider()

# Nasdaq
st.subheader("📈 NASDAQ")
st.metric("Z-Score", f"{data['nas_z']:.2f}")
st.write(data["nas_signal"])

#py -m streamlit run src/app.py