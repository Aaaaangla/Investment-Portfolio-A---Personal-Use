import pandas as pd
import numpy as np


def calculate_cagr(price_series: pd.Series, years: int) -> float | None:
    if price_series is None or price_series.empty:
        return None

    price_series = price_series.dropna()

    end_date = price_series.index.max()
    start_date = end_date - pd.DateOffset(years=years)

    window = price_series[price_series.index >= start_date]

    if len(window) < 2:
        return None

    start_price = float(window.iloc[0])
    end_price = float(window.iloc[-1])

    return (end_price / start_price) ** (1 / years) - 1
