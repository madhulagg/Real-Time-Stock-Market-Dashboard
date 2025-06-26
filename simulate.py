import yfinance as yf
import pandas as pd
from strategies import sma_crossover, momentum_strategy, rsi_strategy

INITIAL_CASH = 2_000_000
SENSEX_30 = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
    "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "AXISBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "HCLTECH.NS", "SUNPHARMA.NS",
    "TATAMOTORS.NS", "WIPRO.NS", "ULTRACEMCO.NS", "TITAN.NS", "BAJFINANCE.NS",
    "NESTLEIND.NS", "POWERGRID.NS", "BAJAJFINSV.NS", "NTPC.NS", "ONGC.NS",
    "TECHM.NS", "ADANIENT.NS", "JSWSTEEL.NS", "COALINDIA.NS", "INDUSINDBK.NS"
]

def fetch_price_data(symbol, period="6mo"):
    df = yf.download(symbol, period=period, group_by='ticker', progress=False)
    if df.empty:
        return {}

    # If MultiIndex, collapse to the symbol level
    if isinstance(df.columns, pd.MultiIndex):
        if symbol in df.columns.get_level_values(0):
            df = df[symbol]
        else:
            df = df.droplevel(0, axis=1)

    df = df.reset_index()

    # Prefer "Adj Close" if available, else "Close"
    price_col = "Adj Close" if "Adj Close" in df.columns else "Close"
    if price_col not in df.columns:
        return {}

    df = df[["Date", price_col]].dropna()
    df["Date"] = pd.to_datetime(df["Date"])
    return {row["Date"].strftime("%Y-%m-%d"): float(row[price_col]) for _, row in df.iterrows()}

def simulate_portfolio(symbols=SENSEX_30, period="6mo"):
    # Load all price data
    price_data = {}
    for sym in symbols:
        try:
            data = fetch_price_data(sym, period)
            if data:  # Only add if we got valid data
                price_data[sym] = data
        except Exception as e:
            print(f"Error processing {sym}: {e}")
            continue

    if not price_data:
        print("No valid price data found")
        return {"cash": INITIAL_CASH, "holdings": {}, "history": []}

    # Get all unique dates
    all_dates = set()
    for prices in price_data.values():
        all_dates.update(prices.keys())
    dates = sorted(list(all_dates))

    portfolio = {"cash": INITIAL_CASH, "holdings": {}, "history": []}

    for date in dates:
        # Step 1: generate signals
        buy_symbols = []
        sell_symbols = []

        for symbol in symbols:
            prices = price_data.get(symbol)
            if not prices or date not in prices:
                continue

            try:
                sma = sma_crossover(prices)
                mom = momentum_strategy(prices)
                rsi = rsi_strategy(prices)

                votes = [sma.get(date, "HOLD"), mom.get(date, "HOLD"), rsi.get(date, "HOLD")]
                buy_votes = votes.count("BUY")
                sell_votes = votes.count("SELL")

                if sell_votes >= 2:
                    sell_symbols.append(symbol)
                elif buy_votes >= 2:
                    buy_symbols.append(symbol)
            except Exception as e:
                print(f"Error calculating signals for {symbol}: {e}")
                continue

        # Step 2: Sell all those with sell_votes ≥ 2
        for symbol in sell_symbols:
            shares = portfolio["holdings"].get(symbol, 0)
            if shares > 0:
                price = price_data[symbol].get(date, 0)
                if price > 0:
                    portfolio["cash"] += shares * price
                    portfolio["holdings"][symbol] = 0

        # Step 3: Distribute equally among buy_symbols
        if buy_symbols:
            budget_per_stock = portfolio["cash"] / len(buy_symbols)
            for symbol in buy_symbols:
                price = price_data[symbol].get(date, 0)
                if price > 0:
                    shares = int(budget_per_stock // price)
                    if shares > 0:
                        portfolio["cash"] -= shares * price
                        portfolio["holdings"][symbol] = portfolio["holdings"].get(symbol, 0) + shares

        # Step 4: Record history
        total_value = portfolio["cash"]
        for symbol in symbols:
            shares = portfolio["holdings"].get(symbol, 0)
            price = price_data.get(symbol, {}).get(date, 0)
            if price > 0:
                total_value += shares * price

        portfolio["history"].append({
            "date": date,
            "cash": round(portfolio["cash"], 2),
            "total": round(total_value, 2),
            "holdings": portfolio["holdings"].copy()
        })

    return portfolio

def simulate(period="6mo", return_history=False):
    portfolio = simulate_portfolio(SENSEX_30, period)
    
    if return_history:
        return portfolio["history"]
    
    final_value = portfolio["history"][-1]["total"] if portfolio["history"] else INITIAL_CASH
    return {
        "initial": INITIAL_CASH,
        "final": final_value,
        "return": final_value - INITIAL_CASH,
        "return_pct": ((final_value - INITIAL_CASH) / INITIAL_CASH) * 100
    }

def get_individual_stock_performance(symbol, period="6mo"):
    """Get performance analysis for individual stock"""
    try:
        prices = fetch_price_data(symbol, period)
        if not prices or len(prices) < 20:
            return None
            
        dates = list(prices.keys())
        price_values = list(prices.values())
        
        # Calculate strategies
        sma_signals = sma_crossover(prices)
        momentum_signals = momentum_strategy(prices)
        rsi_signals = rsi_strategy(prices)
        
        # Get latest signals
        latest_date = dates[-1]
        sma_signal = sma_signals.get(latest_date, "HOLD")
        momentum_signal = momentum_signals.get(latest_date, "HOLD")
        rsi_signal = rsi_signals.get(latest_date, "HOLD")
        
        # Calculate returns
        initial_price = price_values[0]
        final_price = price_values[-1]
        total_return = final_price - initial_price
        total_return_pct = (total_return / initial_price) * 100
        
        # Simulate buy and hold strategy
        shares_bought = int(INITIAL_CASH / initial_price)
        buy_hold_value = shares_bought * final_price
        buy_hold_return = buy_hold_value - INITIAL_CASH
        buy_hold_return_pct = (buy_hold_return / INITIAL_CASH) * 100
        
        return {
            "symbol": symbol,
            "initial_price": round(initial_price, 2),
            "final_price": round(final_price, 2),
            "total_return": round(total_return, 2),
            "total_return_pct": round(total_return_pct, 2),
            "buy_hold_return": round(buy_hold_return, 2),
            "buy_hold_return_pct": round(buy_hold_return_pct, 2),
            "signals": {
                "sma": sma_signal,
                "momentum": momentum_signal,
                "rsi": rsi_signal
            },
            "price_history": {
                "dates": dates,
                "prices": [round(p, 2) for p in price_values]
            }
        }
    except Exception as e:
        print(f"Error in get_individual_stock_performance for {symbol}: {e}")
        return None
