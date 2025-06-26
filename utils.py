def reset_portfolio():
    """Reset portfolio to initial state"""
    default_portfolio = {
        "cash": 2000000,
        "holdings": {},
        "total_value": 2000000,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_history": []
    }
    save_portfolio(default_portfolio)
    return default_portfolio

def execute_automated_trades(analysis_results, portfolio):
    """
    Execute trades based on your specific logic:
    - Sell all stocks that have SELL signals
    - For BUY signals: distribute available cash equally among all buy recommendations
    """
    if not analysis_results or "results" not in analysis_results:
        return {"error": "No analysis results available"}
    
    executed_trades = []
    
    # Step 1: Sell all stocks with SELL signals
    for symbol, analysis in analysis_results["results"].items():
        if analysis["consensus_signal"] == "SELL":
            # Check if we have holdings for this stock
            symbol_key = symbol.replace(".BSE", "")
            if portfolio["holdings"].get(symbol_key, 0) > 0:
                quantity = portfolio["holdings"][symbol_key]
                price = analysis["latest_price"]
                total_value = quantity * price
                
                # Execute sell
                portfolio["cash"] += total_value
                del portfolio["holdings"][symbol_key]
                
                executed_trades.append({
                    "action": "SELL",
                    "symbol": symbol,
                    "price": price,
                    "quantity": quantity,
                    "total": total_value,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    # Step 2: Buy stocks with BUY signals
    buy_recommendations = analysis_results.get("buy_recommendations", [])
    
    if buy_recommendations and portfolio["cash"] > 0:
        # Calculate amount to invest in each stock
        cash_per_stock = portfolio["cash"] / len(buy_recommendations)
        
        for recommendation in buy_recommendations:
            symbol = recommendation["symbol"]
            price = recommendation["price"]
            symbol_key = symbol.replace(".BSE", "")
            
            # Calculate how many shares we can buy
            shares_to_buy = int(cash_per_stock / price)
            
            if shares_to_buy > 0:
                total_cost = shares_to_buy * price
                
                # Execute buy
                portfolio["cash"] -= total_cost
                portfolio["holdings"][symbol_key] = portfolio["holdings"].get(symbol_key, 0) + shares_to_buy
                
                executed_trades.append({
                    "action": "BUY",
                    "symbol": symbol,
                    "price": price,
                    "quantity": shares_to_buy,
                    "total": total_cost,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    # Update portfolio
    portfolio["transaction_history"].extend(executed_trades)
    portfolio["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate total portfolio value
    holdings_value = sum([
        qty * price for qty, price in portfolio["holdings"].items()
    ])
    portfolio["total_value"] = round(portfolio["cash"] + holdings_value, 2)
    
    # Keep only last 100 transactions
    if len(portfolio["transaction_history"]) > 100:
        portfolio["transaction_history"] = portfolio["transaction_history"][-100:]
    
    save_portfolio(portfolio)
    return portfolio

def get_sensex_30_symbols():
    """Return list of Sensex 30 stock symbols"""
    return [
        "RELIANCE.BSE", "TCS.BSE", "HDFCBANK.BSE", "INFY.BSE", "HINDUNILVR.BSE",
        "ICICIBANK.BSE", "SBIN.BSE", "BHARTIARTL.BSE", "ITC.BSE", "KOTAKBANK.BSE",
        "LT.BSE", "ASIANPAINT.BSE", "AXISBANK.BSE", "MARUTI.BSE", "SUNPHARMA.BSE",
        "TITAN.BSE", "ULTRACEMCO.BSE", "NESTLEIND.BSE", "BAJFINANCE.BSE", "WIPRO.BSE",
        "M&M.BSE", "NTPC.BSE", "TECHM.BSE", "POWERGRID.BSE", "HCLTECH.BSE",
        "TATAMOTORS.BSE", "BAJAJFINSV.BSE", "DRREDDY.BSE", "ONGC.BSE", "JSWSTEEL.BSE"
    ]

def calculate_portfolio_performance(portfolio):
    """Calculate portfolio performance metrics"""
    if not portfolio.get("transaction_history"):
        return {
            "total_trades": 0,
            "total_invested": 0,
            "current_value": portfolio.get("total_value", 0),
            "unrealized_pnl": 0,
            "return_percentage": 0
        }
    
    # Calculate total invested amount
    total_invested = sum([
        tx["total"] for tx in portfolio["transaction_history"] 
        if tx["action"] == "BUY"
    ])
    
    total_received = sum([
        tx["total"] for tx in portfolio["transaction_history"] 
        if tx["action"] == "SELL"
    ])
    
    net_invested = total_invested - total_received
    current_value = portfolio.get("total_value", 0)
    
    # Calculate P&L
    unrealized_pnl = current_value - 2000000  # Assuming 2000000 initial capital
    return_percentage = (unrealized_pnl / 2000000) * 100 if unrealized_pnl != 0 else 0
    
    return {
        "total_trades": len(portfolio["transaction_history"]),
        "buy_trades": len([tx for tx in portfolio["transaction_history"] if tx["action"] == "BUY"]),
        "sell_trades": len([tx for tx in portfolio["transaction_history"] if tx["action"] == "SELL"]),
        "total_invested": round(total_invested, 2),
        "total_received": round(total_received, 2),
        "net_invested": round(net_invested, 2),
        "current_value": round(current_value, 2),
        "unrealized_pnl": round(unrealized_pnl, 2),
        "return_percentage": round(return_percentage, 2)
    }

def get_top_holdings(portfolio, limit=10):
    """Get top holdings by value"""
    holdings = portfolio.get("holdings", {})
    if not holdings:
        return []
    
    # For this example, we'll use a placeholder price
    # In a real implementation, you'd fetch current prices
    placeholder_price = 1000
    
    holdings_with_value = [
        {
            "symbol": symbol,
            "quantity": qty,
            "estimated_value": qty * placeholder_price,
            "percentage": (qty * placeholder_price / portfolio["total_value"]) * 100
        }
        for symbol, qty in holdings.items()
    ]
    
    return sorted(holdings_with_value, key=lambda x: x["estimated_value"], reverse=True)[:limit]

def reset_portfolio():
    """Reset portfolio to initial state"""
    default_portfolio = {
        "cash": 100000,
        "holdings": {},
        "total_value": 100000,
        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transaction_history": []
    }
    save_portfolio(default_portfolio)
    return default_portfolio

def export_portfolio_report(portfolio):
    """Export portfolio as detailed report"""
    performance = calculate_portfolio_performance(portfolio)
    top_holdings = get_top_holdings(portfolio)
    
    report = {
        "portfolio_summary": {
            "cash": portfolio["cash"],
            "total_value": portfolio["total_value"],
            "last_updated": portfolio["last_updated"]
        },
        "performance": performance,
        "top_holdings": top_holdings,
        "recent_transactions": portfolio["transaction_history"][-20:],  # Last 20 transactions
        "total_holdings": len(portfolio["holdings"]),
        "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return report

# Price fetching helper (placeholder - you might want to cache these)
def get_current_price(symbol):
    """Get current price for a symbol (placeholder implementation)"""
    # In a real implementation, you would:
    # 1. Cache prices to avoid API calls
    # 2. Use a reliable price source
    # 3. Handle API errors gracefully
    return 1000  # Placeholder price