import json
import os

PORTFOLIO_FILE = "data/portfolio.json"

def load_portfolio():
    if not os.path.exists("portfolio.json") or os.stat("portfolio.json").st_size == 0:
        return {}

    with open("portfolio.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


# def load_portfolio():
#     if not os.path.exists(PORTFOLIO_FILE):
#         return {"cash": 100000, "holdings": {}, "total_value": 100000}
#     with open(PORTFOLIO_FILE, "r") as f:
#         return json.load(f)

def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_portfolio(signals, symbol):
    prices = list(signals.keys())
    portfolio = load_portfolio()

    # Ensure keys exist
    if "cash" not in portfolio:
        portfolio["cash"] = 10000  # or any default initial capital
    if "holdings" not in portfolio:
        portfolio["holdings"] = {}

    latest_price = None

    for date in prices:
        action = signals[date]
        price = float(price_from_date(date, symbol))
        latest_price = price
        if action == "BUY" and portfolio["cash"] >= price:
            portfolio["holdings"][symbol] = portfolio["holdings"].get(symbol, 0) + 1
            portfolio["cash"] -= price
        elif action == "SELL" and portfolio["holdings"].get(symbol, 0) > 0:
            portfolio["holdings"][symbol] -= 1
            portfolio["cash"] += price

    holding_value = sum([latest_price * qty for sym, qty in portfolio["holdings"].items()])
    portfolio["total_value"] = round(portfolio["cash"] + holding_value, 2)

    save_portfolio(portfolio)
    return portfolio


# Dummy function — you need to store daily prices somewhere or modify this
def price_from_date(date, symbol):
    # This should return the closing price for `date`
    # You can enhance this by caching Alpha Vantage data
    return 100  # Placeholder
