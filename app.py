import streamlit as st
import pandas as pd

# ======================
# Import business logic
# ======================
from data.price_loader import (
    load_price_data,
    get_company_name,
    get_company_sector
)

from metrics.cagr import calculate_cagr
from metrics.factors.return_factor import (
    rolling_return_consistency,
    portfolio_return_score
)

from visuals.radar import portfolio_radar_chart
from metrics.factors.risk_factor import portfolio_risk_score

# ======================
# Page config
# ======================
st.set_page_config(
    page_title="Investment Decision Assistant",
    page_icon="📈",
    layout="wide"
)


# ======================
# Session state
# ======================
if "step" not in st.session_state:
    st.session_state.step = "home"


# =========================================================
# STEP 1 — HOME
# =========================================================
if st.session_state.step == "home":

    st.title("📈 Investment Decision Assistant")

    st.write(
        """
        This web application supports **long-term investment decision-making**
        by analysing stocks through **return, risk, and quality-related metrics**.

        The goal is to identify **high-quality core holdings** —
        not to chase short-term price movements.
        """
    )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.step = "select_stocks"
            st.rerun()


# =========================================================
# STEP 2 — SELECT STOCKS
# =========================================================
elif st.session_state.step == "select_stocks":

    st.title("📊 Select Your Stocks")

    st.write(
        """
        Enter the stock tickers you would like to analyse.

        This engine focuses on **long-term investment quality** —
        not short-term trading signals.
        """
    )

    st.markdown("---")

    tickers_input = st.text_input(
        "Enter stock tickers (comma separated)",
        placeholder="e.g. AAPL, MSFT, NVDA, JPM"
    )

    if not tickers_input:
        st.stop()

    ticker_list = [
        t.strip().upper()
        for t in tickers_input.split(",")
        if t.strip()
    ]

    # =================================================
    # BACKEND — Calculate once
    # =================================================
    results = []
    price_data_map = {}   # 为 Risk 因子预留

    for ticker in ticker_list:
        try:
            data = load_price_data(ticker, period="10y")

            if data.empty:
                st.warning(f"No price data found for {ticker}")
                continue

            price_series = data["Adj Close"]
            price_data_map[ticker] = price_series

            # ---------- Return metrics ----------
            cagr_5y = calculate_cagr(price_series, years=5)
            cagr_10y = calculate_cagr(price_series, years=10)

            rolling_consistency = rolling_return_consistency(
                price_series,
                window_years=3
            )

            results.append({
                "Ticker": ticker,
                "Company": get_company_name(ticker),
                "Sector": get_company_sector(ticker),
                "CAGR 5Y (%)": round(cagr_5y * 100, 2) if cagr_5y is not None else None,
                "CAGR 10Y (%)": round(cagr_10y * 100, 2) if cagr_10y is not None else None,
                "Rolling Consistency (%)": round(rolling_consistency, 2)
                if rolling_consistency is not None else None,
            })

        except Exception as e:
            st.error(f"Error processing {ticker}: {e}")

    if not results:
        st.warning("No valid stock data.")
        st.stop()

    df = pd.DataFrame(results)

    # =================================================
    # FRONTEND — Investment Decision Engine
    # =================================================
    st.markdown("---")
    st.subheader("📌 Investment Decision Engine")

    tab_portfolio, tab_stock = st.tabs(["📁 Portfolio", "📊 Stock"])

    # -----------------------------
    # TAB 1 — Portfolio
    # -----------------------------
    with tab_portfolio:
        st.markdown("### 📁 Portfolio Overview")

        st.info(
            """
            This section focuses on **portfolio-level analysis**, such as:

            • Overall return quality  
            • Diversification across sectors  
            • Portfolio risk & stability  
            • Factor balance (radar view)
            """
        )

        # -------- REAL Return factor --------
        return_score = portfolio_return_score(df)
        risk_score = portfolio_risk_score(
            price_data_map,
            profile="growth"   # or "core"
        )

        st.metric(
            label="📈 Portfolio Return Score",
            value=return_score,
            help="Computed from 5Y CAGR, 10Y CAGR and rolling return consistency."
        )

        st.markdown("### 🧭 Portfolio Factor Radar")

        # -------- Factor placeholders --------
        portfolio_factors = {
            "Return": return_score,
            "Risk": risk_score,          # ✅ 真实 Risk
            "Quality": None,
            "Growth": None,
            "Financial Strength": None,
            "Valuation Discipline": None,
        }


        # 用中性值填充未实现因子（保证雷达图稳定）
        portfolio_factors = {
            k: (v if v is not None else 50)
            for k, v in portfolio_factors.items()
        }

        radar_fig = portfolio_radar_chart(portfolio_factors)
        st.plotly_chart(radar_fig, use_container_width=True)

        st.caption(
            "⚠️ Only **Return** is currently computed from real data. "
            "Other factors are placeholders and will be implemented next."
        )

    # -----------------------------
    # TAB 2 — Stock
    # -----------------------------
    with tab_stock:
        st.markdown("### 📊 Stock-Level Analysis")
        st.dataframe(df, use_container_width=True)

    # =================================================
    # Footer
    # =================================================
    st.markdown("---")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅ Back"):
            st.session_state.step = "home"
            st.rerun()
