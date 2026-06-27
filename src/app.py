import streamlit as st
import yfinance as yf

from trade_logger import log_trade
from performance_analyzer import (
    load_trades,
    equity_curve,
    drawdown,
    win_rate,
    total_pnl,
    pnl_by_asset
)
from risk_calculator import (
    calculate_risk,
    calculate_position_size,
    calculate_risk_reward,
    portfolio_exposure
)
from stat_arb_engine import run_all


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="DQL Quant Terminal",
    page_icon="📈",
    layout="wide"
)

st.title("📊 DQL Quant Terminal")
st.caption("Professional Risk Management & Quantitative Research Platform")

st.divider()
st.subheader("🌍 Live Market Watch")


# -----------------------------
# CACHED MARKET DATA ENGINE (IMPORTANT FIX)
# -----------------------------
@st.cache_data(ttl=10)
def get_market_summary(ticker):
    data = yf.Ticker(ticker).history(period="1d", interval="1m")

    if data is None or data.empty:
        return {
            "price": None,
            "change": None,
            "high": None,
            "low": None
        }

    last_price = data["Close"].iloc[-1]
    open_price = data["Open"].iloc[0]

    high = data["High"].max()
    low = data["Low"].min()

    change = ((last_price - open_price) / open_price) * 100 if open_price else None

    return {
        "price": float(last_price),
        "change": float(change) if change is not None else None,
        "high": float(high),
        "low": float(low)
    }


# -----------------------------
# SAFE FORMATTER
# -----------------------------
def fmt(val, suffix=""):
    try:
        if val is None:
            return "N/A"
        return f"{float(val):.2f}{suffix}"
    except:
        return "N/A"


# -----------------------------
# MARKET DATA
# -----------------------------
btc = get_market_summary("BTC-USD")
eth = get_market_summary("ETH-USD")
gold = get_market_summary("GC=F")
nasdaq = get_market_summary("^IXIC")


# -----------------------------
# UI METRICS
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("₿ BTCUSD", f"${fmt(btc['price'])}", f"{fmt(btc['change'], '%')}")

with c2:
    st.metric("Ξ ETHUSD", f"${fmt(eth['price'])}", f"{fmt(eth['change'], '%')}")

with c3:
    st.metric("🥇 GOLD", f"${fmt(gold['price'])}", f"{fmt(gold['change'], '%')}")

with c4:
    st.metric("📈 NASDAQ", f"{fmt(nasdaq['price'])}", f"{fmt(nasdaq['change'], '%')}")


# -----------------------------
# HIGH / LOW PANEL
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.caption(f"High: {fmt(btc['high'])}")
    st.caption(f"Low : {fmt(btc['low'])}")

with col2:
    st.caption(f"High: {fmt(eth['high'])}")
    st.caption(f"Low : {fmt(eth['low'])}")

with col3:
    st.caption(f"High: {fmt(gold['high'])}")
    st.caption(f"Low : {fmt(gold['low'])}")

with col4:
    st.caption(f"High: {fmt(nasdaq['high'])}")
    st.caption(f"Low : {fmt(nasdaq['low'])}")

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
st.subheader("Risk Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Risk Amount",
        f"${risk_amount:.2f}"
    )

with col2:
    st.metric(
        "Position Size",
        f"{position:.4f}"
    )

with col3:
    st.metric(
        "Risk : Reward",
        f"{rr:.2f}"
    )

with col4:
    st.metric(
        "Portfolio Exposure",
        f"{portfolio_exposure([risk_amount,15,10])}%"
    )

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

left_col, right_col = st.columns([2, 1])

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