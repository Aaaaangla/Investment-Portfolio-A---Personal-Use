import pandas as pd
import numpy as np

from benchmarks.return_benchmarks import RETURN_BENCHMARKS
from metrics.normalization import normalise

# =====================================================
# Rolling CAGR
# =====================================================
def rolling_cagr(
    price_series: pd.Series,
    window_years: int = 3
) -> pd.Series:
    """
    Compute rolling CAGR over a given window (years).
    Returns CAGR as decimal (e.g. 0.12 = 12%).
    """
    window_days = window_years * 252
    return (price_series / price_series.shift(window_days)) ** (1 / window_years) - 1


# =====================================================
# Rolling Return Consistency
# =====================================================
def rolling_return_consistency(
    price_series: pd.Series,
    window_years: int = 3
) -> float | None:
    """
    Percentage of rolling periods with positive CAGR.
    Output: 0–100
    """
    rc = rolling_cagr(price_series, window_years).dropna()

    if rc.empty:
        return None

    return (rc > 0).mean() * 100


# =====================================================
# Portfolio-level Return Factor
# =====================================================
def portfolio_return_score(df: pd.DataFrame) -> float:
    """
    Compute portfolio-level Return factor score (0–100).

    Components:
    - CAGR 5Y (growth quality)
    - CAGR 10Y (durability)
    - Rolling Return Consistency (stability)

    Scoring logic:
    Linear normalisation using RETURN_BENCHMARKS.
    See overall_rules.md for interpretation.
    """

    def safe_mean(series: pd.Series) -> float | None:
        s = pd.to_numeric(series, errors="coerce").dropna()
        return s.mean() if not s.empty else None

    # -----------------------------
    # Raw metrics (portfolio mean)
    # -----------------------------
    cagr_5y = safe_mean(df.get("CAGR 5Y (%)"))
    cagr_10y = safe_mean(df.get("CAGR 10Y (%)"))
    consistency = safe_mean(df.get("Rolling Consistency (%)"))  # already 0–100

    scores: list[float] = []

    # -----------------------------
    # Normalised scores (0–100)
    # -----------------------------
    if cagr_5y is not None:
        cfg = RETURN_BENCHMARKS["cagr_5y"]
        score = normalise(
            cagr_5y / 100,   # % → decimal
            cfg["worst"],
            cfg["best"]
        )
        scores.append(score)

    if cagr_10y is not None:
        cfg = RETURN_BENCHMARKS["cagr_10y"]
        score = normalise(
            cagr_10y / 100,
            cfg["worst"],
            cfg["best"]
        )
        scores.append(score)

    if consistency is not None:
        cfg = RETURN_BENCHMARKS["consistency"]
        score = normalise(
            consistency / 100,
            cfg["worst"],
            cfg["best"]
        )
        scores.append(score)

    if not scores:
        return 0.0

    return round(float(np.mean(scores)), 1)
