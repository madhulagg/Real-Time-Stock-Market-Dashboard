import yfinance as yf
import pandas as pd
from strategies import sma_crossover, momentum_strategy, rsi_strategy
from utils import load_portfolio, save_portfolio
import matplotlib.pyplot as plt

INITIAL_CASH = 2000000
SENSEX_30 = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "LT.NS", "SBIN.NS", "BAJFINANCE.NS",
    "ASIANPAINT.NS", "AXISBANK.NS", "HCLTECH.NS", "KOTAKBANK.NS", "MARUTI.NS",
    "SUNPHARMA.NS", "NTPC.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "TITAN.NS",
    "POWERGRID.NS", "WIPRO.NS", "TECHM.NS", "BAJAJFINSV.NS", "JSWSTEEL.NS",
    "M&M.NS", "TATASTEEL.NS", "BHARTIARTL.NS", "HDFCLIFE.NS", "ONGC.NS"
]

def fetch_price_data(symbols, period="6mo"):
    data = yf.download(symbols, period=period, group_by='ticker', auto_adjust=True)
    price_data = {}
    for symbol in symbols:
        df = data[symbol] if isinstance(data.columns, pd.MultiIndex) else data
        if 'Close' in df:
            df = df.reset_index()
            price_data[symbol] = {row['Date'].strftime("%Y-%m-%d"): float(row['Close']) for _, row in df.iterrows()}
    return price_data

def combine_signals(date, strategy_outputs):
    votes = [signals.get(date, "HOLD") for signals in strategy_outputs]
    return votes.count("BUY"), votes.count("SELL")


def plot_portfolio_history(portfolio_history):
    dates = [entry["date"] for entry in portfolio_history]
    values = [entry["total_value"] for entry in portfolio_history]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, label="Your Strategy", linewidth=2)
    plt.title("📈 Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (₹)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def simulate_sensex_strategy(period="6mo"):
    price_data = fetch_price_data(SENSEX_30, period)
    dates = sorted(list(next(iter(price_data.values())).keys()))

    signals = {}
    for stock in SENSEX_30:
        if stock in price_data:
            signals[stock] = {
                'sma': sma_crossover(price_data[stock]),
                'momentum': momentum_strategy(price_data[stock]),
                'rsi': rsi_strategy(price_data[stock])
            }

    portfolio = {"cash": INITIAL_CASH, "holdings": {}, "history": []}

    for date in dates:
        # First: sell all stocks with ≥2 sell votes
        for stock in SENSEX_30:
            if stock in price_data and date in price_data[stock]:
                _, sell_votes = combine_signals(date, [signals[stock]['sma'], signals[stock]['momentum'], signals[stock]['rsi']])
                if sell_votes >= 2:
                    shares = portfolio["holdings"].get(stock, 0)
                    if shares > 0:
                        portfolio["cash"] += shares * price_data[stock][date]
                        portfolio["holdings"][stock] = 0

        # Then: count how many BUYs today
        buy_candidates = []
        for stock in SENSEX_30:
            if stock in price_data and date in price_data[stock]:
                buy_votes, _ = combine_signals(date, [signals[stock]['sma'], signals[stock]['momentum'], signals[stock]['rsi']])
                if buy_votes >= 2:
                    buy_candidates.append(stock)

        # Distribute cash equally among buy candidates
        if buy_candidates:
            budget_per_stock = portfolio["cash"] / len(buy_candidates)
            for stock in buy_candidates:
                price = price_data[stock][date]
                if price > 0:
                    num_shares = int(budget_per_stock // price)
                    if num_shares > 0:
                        cost = num_shares * price
                        portfolio["cash"] -= cost
                        portfolio["holdings"][stock] = portfolio["holdings"].get(stock, 0) + num_shares

        # Log portfolio value
        total_val = portfolio["cash"]
        for stock in SENSEX_30:
            if stock in price_data and date in price_data[stock]:
                total_val += portfolio["holdings"].get(stock, 0) * price_data[stock][date]

        portfolio["history"].append({
            "date": date,
            "cash": round(portfolio["cash"], 2),
            "total_value": round(total_val, 2)
        })

    save_portfolio(portfolio)

    final = portfolio["history"][-1]["total_value"]
    profit = final - INITIAL_CASH
    return_pct = (profit / INITIAL_CASH) * 100

    print(f"\n✅ Final Portfolio Value: ₹{final:,.2f}")
    print(f"📈 Total Profit: ₹{profit:,.2f}")
    print(f"📊 Return: {return_pct:.2f}%")
    plot_portfolio_history(portfolio["history"])


if __name__ == "__main__":
    simulate_sensex_strategy(period="6mo")

