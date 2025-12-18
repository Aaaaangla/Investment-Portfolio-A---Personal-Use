import streamlit as st

from data.stock_universe import get_all_tickers
from data.price_loader import load_price_data
from metrics.risk_metrics import calculate_cagr, calculate_volatility
from models.stock_classifier import classify_stock

st.set_page_config(
    page_title="Personal Investment Engine",
    layout="centered"
)

st.title("🧠 Stock Type Classification Engine")
st.caption("Rule-based | Risk-aware | Long-term focused")
st.divider()

# ======================
# UI
# ======================
ticker = st.selectbox(
    "Choose a stock ticker",
    options=get_all_tickers()
)

period = st.selectbox(
    "Analysis period",
    options=["3y", "5y", "10y"],
    index=1
)

if st.button("Run Classification"):
    prices = load_price_data(ticker, period)

    metrics = {
        "CAGR": calculate_cagr(prices),
        "Volatility": calculate_volatility(prices)
    }

    stock_type = classify_stock(metrics)

    st.subheader("📊 Result")
    st.write(f"**Stock:** {ticker}")
    st.write(f"**Type:** {stock_type}")
