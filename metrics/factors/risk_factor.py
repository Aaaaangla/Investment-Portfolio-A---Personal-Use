import numpy as np
import pandas as pd

from benchmarks.risk_benchmarks import RISK_BENCHMARKS
from metrics.normalization import normalise_inverse


# =====================================================
# Risk raw metrics (single asset)
# =====================================================
def max_drawdown(price_series: pd.Series) -> float | None:
    """
    Max drawdown as a positive decimal.
    Example: 0.35 represents a -35% drawdown.
    """
    if price_series is None or price_series.empty:
        return None

    cum_max = price_series.cummax()
    drawdown = (price_series - cum_max) / cum_max
    return abs(drawdown.min())


def annualised_volatility(price_series: pd.Series) -> float | None:
    """
    Annualised volatility (decimal).
    """
    if price_series is None or price_series.empty:
        return None

    returns = price_series.pct_change().dropna()
    return returns.std() * np.sqrt(252)


def downside_volatility(price_series: pd.Series) -> float | None:
    """
    Annualised downside volatility (decimal).
    Measures volatility of negative returns only.
    """
    if price_series is None or price_series.empty:
        return None

    returns = price_series.pct_change().dropna()
    downside = returns[returns < 0]

    if downside.empty:
        # No downside volatility observed
        return 0.0

    return downside.std() * np.sqrt(252)


# =====================================================
# Portfolio-level Risk Factor
# =====================================================
def portfolio_risk_score(
    price_data_map: dict[str, pd.Series],
    profile: str = "growth"
) -> float:
    """
    Compute portfolio-level Risk score (0–100).

    Parameters
    ----------
    price_data_map : dict[str, pd.Series]
        Mapping from ticker to adjusted close price series.
    profile : str
        Risk profile to use for benchmarking.
        Options: "core", "growth", "aggressive"

    Interpretation
    --------------
    Higher score = lower historical risk *relative to the selected profile*.
    """

    if profile not in RISK_BENCHMARKS:
        raise ValueError(
            f"Unknown risk profile '{profile}'. "
            f"Available profiles: {list(RISK_BENCHMARKS.keys())}"
        )

    mdd_list = []
    vol_list = []
    dvol_list = []

    # -------------------------------------------------
    # Collect raw risk metrics for each asset
    # -------------------------------------------------
    for series in price_data_map.values():
        mdd = max_drawdown(series)
        vol = annualised_volatility(series)
        dvol = downside_volatility(series)

        if mdd is not None:
            mdd_list.append(mdd)
        if vol is not None:
            vol_list.append(vol)
        if dvol is not None:
            dvol_list.append(dvol)

    scores = []
    profile_cfg = RISK_BENCHMARKS[profile]

    # -------------------------------------------------
    # Max Drawdown (psychological risk)
    # -------------------------------------------------
    if mdd_list:
        cfg = profile_cfg["max_drawdown"]
        mdd_score = normalise_inverse(
            value=np.mean(mdd_list),
            best=cfg["best"],
            worst=cfg["worst"]
        )
        scores.append(mdd_score)

    # -------------------------------------------------
    # Volatility (total risk)
    # -------------------------------------------------
    if vol_list:
        cfg = profile_cfg["volatility"]
        vol_score = normalise_inverse(
            value=np.mean(vol_list),
            best=cfg["best"],
            worst=cfg["worst"]
        )
        scores.append(vol_score)

    # -------------------------------------------------
    # Downside Volatility (bad volatility)
    # -------------------------------------------------
    if dvol_list:
        cfg = profile_cfg["downside_volatility"]
        dvol_score = normalise_inverse(
            value=np.mean(dvol_list),
            best=cfg["best"],
            worst=cfg["worst"]
        )
        scores.append(dvol_score)

    if not scores:
        return 0.0

    return round(float(np.mean(scores)), 1)
