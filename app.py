from flask import Flask, render_template, request, jsonify
import yfinance as yf
from simulate import simulate, get_individual_stock_performance, SENSEX_30
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/portfolio-overview")
def portfolio_overview():
    period = request.args.get("period", "6mo")
    
    # Get portfolio performance
    portfolio_perf = simulate(period=period)
    
    # Get individual stock performances
    stock_performances = []
    for symbol in SENSEX_30:
        perf = get_individual_stock_performance(symbol, period)
        if perf:
            stock_performances.append(perf)
    
    # Sort by return percentage
    stock_performances.sort(key=lambda x: x["total_return_pct"], reverse=True)
    
    return jsonify({
        "portfolio": portfolio_perf,
        "stocks": stock_performances,
        "total_stocks": len(stock_performances)
    })

@app.route("/api/stock-analysis")
def stock_analysis():
    symbol = request.args.get("symbol", "RELIANCE.NS")
    period = request.args.get("period", "6mo")
    
    # Get individual stock performance
    stock_perf = get_individual_stock_performance(symbol, period)
    
    if not stock_perf:
        return jsonify({"error": "Unable to fetch data for this stock"}), 400
    
    return jsonify(stock_perf)

@app.route("/compare")
def compare():
    symbol = request.args.get("symbol", "RELIANCE.NS")
    
    # Simulate our strategy (returns history)
    history = simulate(period="6mo", return_history=True)
    dates = [entry["date"] for entry in history]
    strategy_values = [entry["total"] for entry in history]

    # Fetch stock price data
    df = yf.download(symbol, period="6mo", interval="1d", progress=False)
    df = df.reset_index()
    df = df[df["Date"].isin(pd.to_datetime(dates))]  # Align with strategy dates
    stock_prices = df["Adj Close" if "Adj Close" in df.columns else "Close"].tolist()
    stock_dates = df["Date"].dt.strftime("%Y-%m-%d").tolist()

    # Normalize both to start at 100
    def normalize(values):
        base = values[0]
        return [round((v / base) * 100, 2) for v in values]

    strategy_norm = normalize(strategy_values)
    stock_norm = normalize(stock_prices)

    return jsonify({
        "dates": stock_dates,
        "strategy": strategy_norm,
        "stock": stock_norm
    })

@app.route("/api/strategy-comparison")
def strategy_comparison():
    period = request.args.get("period", "6mo")
    
    # Get portfolio performance with our 3-strategy approach
    portfolio_perf = simulate(period=period)
    
    # Calculate buy-and-hold performance for Sensex
    try:
        # Use a representative index or calculate average of all stocks
        sensex_data = yf.download("^BSESN", period=period, progress=False)
        if len(sensex_data) > 0:
            initial_sensex = sensex_data.iloc[0]["Close"]
            final_sensex = sensex_data.iloc[-1]["Close"]
            sensex_return_pct = ((final_sensex - initial_sensex) / initial_sensex) * 100
            buy_hold_return = (sensex_return_pct / 100) * 2000000
        else:
            sensex_return_pct = 0
            buy_hold_return = 0
    except:
        sensex_return_pct = 0
        buy_hold_return = 0
    
    return jsonify({
        "strategy_performance": {
            "initial": portfolio_perf["initial"],
            "final": portfolio_perf["final"],
            "return": portfolio_perf["return"],
            "return_pct": portfolio_perf["return_pct"]
        },
        "buy_hold_performance": {
            "initial": 2000000,
            "final": 2000000 + buy_hold_return,
            "return": buy_hold_return,
            "return_pct": sensex_return_pct
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
