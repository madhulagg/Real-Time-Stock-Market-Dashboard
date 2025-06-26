from flask import Flask, render_template, request, jsonify
import requests
from strategies import generate_signals
from utils import update_portfolio
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("ALPHA_API_KEY") 
print("✅ API Key Loaded:", API_KEY)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/stock', methods=['POST'])
def get_stock_data():
    symbol = request.form['symbol'].upper()
    strategy = request.form['strategy']
    
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json()

    if "Time Series (Daily)" not in data : 
        return jsonify({"error": "Invalid symbol or API Limit Reached"})
    prices = {date: float(info['4. close']) for date, info in data['Time Series (Daily)'].items()}
    sorted_prices = dict(sorted(prices.items())[-30:])
    signals = generate_signals(sorted_prices, strategy)
    portfolio = update_portfolio(signals, symbol)

    return jsonify({
        "prices": sorted_prices,
        "signals": signals,
        "portfolio": portfolio
    })

if __name__ == '__main__':
    app.run(debug=True)