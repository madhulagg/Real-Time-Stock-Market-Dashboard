import json
import os

PORTFOLIO_FILE = "portfolio.json"
PRICE_CACHE = {}

def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE) or os.stat(PORTFOLIO_FILE).st_size == 0:
        return {"cash": 100000, "holdings": {}, "total_value": 100000}
    with open(PORTFOLIO_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"cash": 100000, "holdings": {}, "total_value": 100000}

def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_portfolio(signals, symbol):
    portfolio = load_portfolio()
    portfolio.setdefault("cash", 100000)
    portfolio.setdefault("holdings", {})

    latest_price = None

    for date, action in signals.items():
        price = float(price_from_date(date, symbol))
        latest_price = price
        if action == "BUY" and portfolio["cash"] >= price:
            portfolio["holdings"][symbol] = portfolio["holdings"].get(symbol, 0) + 1
            portfolio["cash"] -= price
        elif action == "SELL" and portfolio["holdings"].get(symbol, 0) > 0:
            portfolio["holdings"][symbol] -= 1
            portfolio["cash"] += price

    holding_value = sum(latest_price * qty for qty in portfolio["holdings"].values())
    portfolio["total_value"] = round(portfolio["cash"] + holding_value, 2)

    save_portfolio(portfolio)
    return portfolio

def price_from_date(date, symbol):
    if symbol not in PRICE_CACHE:
        import yfinance as yf
        df = yf.download(symbol, period="90d")
        PRICE_CACHE[symbol] = {
            row.Date.strftime("%Y-%m-%d"): float(row.Close)
            for _, row in df.reset_index().iterrows()
        }
    return PRICE_CACHE[symbol].get(date, 0)
