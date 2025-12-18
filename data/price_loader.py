# data/price_loader.py

import yfinance as yf

def load_price_data(ticker: str, period: str = "5y"):
    """
    Load adjusted close price data from yfinance
    """
    df = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data returned for {ticker}")

    return df["Close"]
