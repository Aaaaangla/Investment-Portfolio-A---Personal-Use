# data/stock_universe.py

STOCK_UNIVERSE = {
    "US Mega Cap": [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "NVDA",
        "META",
        "ORCL"
    ],
    "Semiconductors": [
        "NVDA",
        "AMD",
        "INTC",
        "TSM",
        "AVGO"
    ]
}

def get_all_tickers():
    """Return a sorted unique list of all tickers"""
    tickers = set()
    for group in STOCK_UNIVERSE.values():
        tickers.update(group)
    return sorted(list(tickers))