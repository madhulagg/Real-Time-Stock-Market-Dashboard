import yfinance as yf
import pandas as pd
import json
import os
from strategies import sma_crossover, momentum_strategy, rsi_strategy
from utils import load_portfolio, save_portfolio

INITIAL_CASH = 2_000_000
STOCK_SYMBOL = "RELIANCE.NS"
PORTFOLIO_FILE = "portfolio.json"

def fetch_price_data(symbol, period="6mo"):
    df = yf.download(symbol, period=period, group_by='ticker')
    
    if isinstance(df.columns, pd.MultiIndex):
        df = df[symbol]  # Collapse the outer symbol level
    
    df = df.reset_index()
    df = df[["Date", "Close"]]  # Keep only relevant columns
    df["Date"] = pd.to_datetime(df["Date"])
    return {row["Date"].strftime("%Y-%m-%d"): float(row["Close"]) for _, row in df.iterrows()}


def combine_signals(date, strategy_outputs):
    votes = [signals.get(date, "HOLD") for signals in strategy_outputs]
    buy_votes = votes.count("BUY")
    sell_votes = votes.count("SELL")
    return buy_votes, sell_votes

def simulate(period="6mo"):
    prices = fetch_price_data(STOCK_SYMBOL, period)
    dates = sorted(prices.keys())

    sma_signals = sma_crossover(prices)
    momentum_signals = momentum_strategy(prices)
    rsi_signals = rsi_strategy(prices)

    portfolio = {"cash": INITIAL_CASH, "holdings": {}, "history": []}

    for date in dates:
        buy_votes, sell_votes = combine_signals(date, [sma_signals, momentum_signals, rsi_signals])
        price = float(prices[date])
        shares = portfolio["holdings"].get(STOCK_SYMBOL, 0)
        action = "HOLD"

        # Buy logic: buy all-in if 2 or more buy votes
        if buy_votes >= 2 and portfolio["cash"] >= price:
            num_shares = int(portfolio["cash"] // price)
            portfolio["cash"] -= num_shares * price
            portfolio["holdings"][STOCK_SYMBOL] = shares + num_shares
            action = f"BUY {num_shares}"

        # Sell logic
        elif sell_votes == 2 and shares > 0:
            num_shares = shares // 2
            portfolio["cash"] += num_shares * price
            portfolio["holdings"][STOCK_SYMBOL] = shares - num_shares
            action = f"SELL {num_shares}"

        elif sell_votes == 3 and shares > 0:
            portfolio["cash"] += shares * price
            portfolio["holdings"][STOCK_SYMBOL] = 0
            action = f"SELL ALL {shares}"

        holding_val = portfolio["holdings"].get(STOCK_SYMBOL, 0) * price
        total_value = round(portfolio["cash"] + holding_val, 2)

        portfolio["history"].append({
            "date": date,
            "action": action,
            "cash": round(portfolio["cash"], 2),
            "holding_value": round(holding_val, 2),
            "total": total_value
        })

    save_portfolio(portfolio)

    final_value = portfolio["history"][-1]["total"]
    total_shares = portfolio["holdings"].get(STOCK_SYMBOL, 0)
    cash_left = round(portfolio["cash"], 2)
    profit = final_value - INITIAL_CASH
    return_pct = (profit / INITIAL_CASH) * 100

    print(f"\n✅ Final Value: ₹{final_value:,.2f}")
    print(f"📅 Final Holdings: {total_shares} shares")
    print(f"💼 Cash Left: ₹{cash_left:,.2f}")
    print(f"📈 Profit: ₹{profit:,.2f}")
    print(f"📊 Return: {return_pct:.2f}%")


if __name__ == "__main__":
    simulate(period="12mo")  # Change to "1mo", "3mo", etc. as needed
