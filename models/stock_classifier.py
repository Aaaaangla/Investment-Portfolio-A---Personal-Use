# models/stock_classifier.py

from config.thresholds import THRESHOLDS

def classify_stock(metrics: dict):
    cagr = metrics["CAGR"]
    vol = metrics["Volatility"]

    if cagr >= THRESHOLDS["core"]["min_cagr"] and vol <= THRESHOLDS["core"]["max_vol"]:
        return "🟢 Core Stable Asset"

    if cagr >= THRESHOLDS["growth"]["min_cagr"] and vol > THRESHOLDS["growth"]["min_vol"]:
        return "🟡 Growth / Momentum Asset"

    return "⚪ Unclassified"
