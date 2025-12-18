import streamlit as st
import pandas as pd

from data.price_loader import (
    load_price_data,
    get_company_name,
    get_company_sector
)

from metrics.cagr import calculate_cagr


st.title("📌 Stock Selection")

tickers = st.text_input(
    "Enter stock tickers (comma separated)",
    placeholder="e.g. AAPL, MSFT, NVDA"
)

if tickers:
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    results = []

    for ticker in ticker_list:
        try:
            data = load_price_data(ticker, period="10y")
            if data.empty:
                continue

            company = get_company_name(ticker)
            sector = get_company_sector(ticker)

            cagr_5y = calculate_cagr(data["Adj Close"], years=5)
            cagr_10y = calculate_cagr(data["Adj Close"], years=10)

            results.append({
                "Ticker": ticker,
                "Company": company,
                "Sector": sector,
                "CAGR 5Y (%)": round(cagr_5y * 100, 2),
                "CAGR 10Y (%)": round(cagr_10y * 100, 2)
            })

        except Exception as e:
            st.error(f"Error processing {ticker}: {e}")

    if results:
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
