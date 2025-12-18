import numpy as np


def normalise(
    value: float,
    worst: float,
    best: float
) -> float:
    """
    Linear normalisation to 0–100 (higher is better)
    """

    if value is None or np.isnan(value):
        return 0.0

    if value <= worst:
        return 0.0

    if value >= best:
        return 100.0

    score = 100 * (value - worst) / (best - worst)
    return round(float(score), 1)


def normalise_inverse(
    value: float,
    best: float,
    worst: float
) -> float:
    """
    Inverse normalisation to 0–100 (lower is better)
    """

    if value is None or np.isnan(value):
        return 0.0

    if value <= best:
        return 100.0

    if value >= worst:
        return 0.0

    score = 100 * (worst - value) / (worst - best)
    return round(float(score), 1)
