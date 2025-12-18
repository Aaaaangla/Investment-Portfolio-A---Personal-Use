import yfinance as yf
import pandas as pd
import streamlit as st


# =========================
# Price Data (Cached)
# =========================
@st.cache_data(ttl=60 * 60 * 24)
def load_price_data(
    ticker: str,
    period: str = "10y"
) -> pd.DataFrame:
    """
    Load historical price data using yfinance.
    Returns a DataFrame with an 'Adj Close' column.
    Cached to avoid repeated API calls.
    """

    data = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=True
    )

    if data.empty:
        return data

    # auto_adjust=True → Close is already adjusted
    data = data.rename(columns={"Close": "Adj Close"})

    return data


# =========================
# Company Metadata (Cached)
# =========================
@st.cache_data(ttl=60 * 60 * 24)
def get_company_metadata(ticker: str) -> dict:
    """
    Fetch company name and sector in ONE API call.
    Cached for performance.
    """

    try:
        info = yf.Ticker(ticker).info
        return {
            "company": info.get("longName", ticker),
            "sector": info.get("sector", "Unknown")
        }
    except Exception:
        return {
            "company": ticker,
            "sector": "Unknown"
        }


# =========================
# Backward-compatible helpers
# =========================
def get_company_name(ticker: str) -> str:
    return get_company_metadata(ticker)["company"]


def get_company_sector(ticker: str) -> str:
    return get_company_metadata(ticker)["sector"]
