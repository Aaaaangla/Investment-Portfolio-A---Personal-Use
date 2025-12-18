import streamlit as st

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Personal Investment Engine",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===============================
# Title
# ===============================
st.title("🧠 Stock Type Classification Engine")
st.caption("Rule-based | Risk-aware | Long-term focused")

st.divider()

# ===============================
# User Input
# ===============================
st.subheader("📌 Select Stock")

stock = st.selectbox(
    "Choose a stock ticker",
    options=["NVDA", "AAPL", "MSFT", "GOOGL", "ORCL"],
    index=0
)

analysis_period = st.selectbox(
    "Analysis period",
    options=["3Y", "5Y", "10Y"],
    index=1
)

run_btn = st.button("Run Classification")

# ===============================
# Mock Metrics (Placeholder)
# Later: replace with real calculations
# ===============================
def get_mock_metrics(ticker):
    """
    Temporary placeholder.
    Later this will be replaced by real data + metrics calculation.
    """
    mock_data = {
        "NVDA": {
            "CAGR": 0.38,
            "Volatility": 0.45,
            "MaxDrawdown": -0.52,
            "Beta": 1.9,
            "Sharpe": 1.1
        },
        "AAPL": {
            "CAGR": 0.18,
            "Volatility": 0.22,
            "MaxDrawdown": -0.32,
            "Beta": 1.1,
            "Sharpe": 1.4
        },
        "ORCL": {
            "CAGR": 0.14,
            "Volatility": 0.20,
            "MaxDrawdown": -0.28,
            "Beta": 0.9,
            "Sharpe": 1.3
        }
    }
    return mock_data.get(ticker, None)

# ===============================
# Classification Logic (v1.0)
# ===============================
def classify_stock(metrics):
    cagr = metrics["CAGR"]
    vol = metrics["Volatility"]
    mdd = metrics["MaxDrawdown"]
    beta = metrics["Beta"]
    sharpe = metrics["Sharpe"]

    reasons = []

    if cagr >= 0.15 and vol <= 0.25 and mdd >= -0.35:
        stock_type = "🟢 Core Stable Asset"
        reasons.append("Strong long-term return")
        reasons.append("Controlled volatility")
        reasons.append("Acceptable drawdown profile")

    elif cagr >= 0.20 and vol > 0.30 and beta > 1.3:
        stock_type = "🟡 Growth / Momentum Asset"
        reasons.append("High growth potential")
        reasons.append("High volatility")
        reasons.append("Market-sensitive (high beta)")

    elif vol <= 0.20 and beta < 1.0:
        stock_type = "🔵 Defensive Asset"
        reasons.append("Low volatility")
        reasons.append("Defensive beta profile")

    elif vol > 0.40 and mdd < -0.50:
        stock_type = "🔴 Speculative / Tactical Asset"
        reasons.append("Extreme volatility")
        reasons.append("Deep historical drawdowns")

    else:
        stock_type = "⚪ Unqualified / Unstable Asset"
        reasons.append("Risk-return profile not suitable for core use")

    return stock_type, reasons

# ===============================
# Run Analysis
# ===============================
if run_btn:
    metrics = get_mock_metrics(stock)

    if metrics is None:
        st.error("No data available for this stock.")
    else:
        stock_type, reasons = classify_stock(metrics)

        st.divider()
        st.subheader("📊 Classification Result")

        st.markdown(f"**Stock:** `{stock}`")
        st.markdown(f"**Type:** {stock_type}")

        st.markdown("**Key Reasons:**")
        for r in reasons:
            st.markdown(f"- {r}")

        st.divider()

        st.markdown("**Raw Metrics (preview):**")
        st.json(metrics)

        st.caption("⚠ This is a rule-based classification model (v0.1). No buy/sell signal is generated.")
