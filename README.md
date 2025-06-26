# Stock Market Dashboard - Sensex 30 Strategy Analysis

A comprehensive full-stack web application that analyzes Sensex 30 stocks using three different trading strategies and tracks portfolio performance with a ₹20 lakh initial investment.

## 🚀 Features

### 📊 Portfolio Overview
- **Real-time Portfolio Tracking**: Monitor your ₹20 lakh investment across Sensex 30 stocks
- **Performance Analytics**: Track total returns, percentage gains/losses, and portfolio value over time
- **Interactive Charts**: Visualize portfolio growth with dynamic charts
- **Top Performers**: View the best-performing stocks in your portfolio

### 📈 Individual Stock Analysis
- **Detailed Stock Analysis**: Analyze any individual Sensex 30 stock
- **Price History**: View historical price movements with interactive charts
- **Trading Signals**: Get BUY/SELL/HOLD recommendations from three strategies
- **Performance Comparison**: Compare stock performance against buy-and-hold strategy

### ⚖️ Strategy Comparison
- **3-Strategy Approach**: Combines SMA Crossover, Momentum, and RSI strategies
- **Buy & Hold Benchmark**: Compare against traditional buy-and-hold Sensex performance
- **Performance Metrics**: Detailed return analysis and risk assessment

## 🎯 Trading Strategies

### 1. SMA Crossover Strategy
- **Short SMA**: 5-day Simple Moving Average
- **Long SMA**: 10-day Simple Moving Average
- **Signal**: BUY when short SMA > long SMA, SELL when short SMA < long SMA

### 2. Momentum Strategy
- **Period**: 10-day momentum calculation
- **Signal**: BUY when price momentum is positive, SELL when negative

### 3. RSI Strategy
- **Period**: 14-day Relative Strength Index
- **Signal**: BUY when RSI < 30 (oversold), SELL when RSI > 70 (overbought)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Data Source**: Yahoo Finance (yfinance)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome

## 📋 Sensex 30 Stocks

The dashboard analyzes all 30 stocks in the BSE Sensex index:
- RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK
- HINDUNILVR, ITC, SBIN, BHARTIARTL, KOTAKBANK
- AXISBANK, ASIANPAINT, MARUTI, HCLTECH, SUNPHARMA
- TATAMOTORS, WIPRO, ULTRACEMCO, TITAN, BAJFINANCE
- NESTLEIND, POWERGRID, BAJAJFINSV, NTPC, ONGC
- TECHM, ADANIENT, JSWSTEEL, COALINDIA, INDUSINDBK

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Real-Time-Stock-Market-Dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the dashboard**
   - Open your browser and go to `http://localhost:5000`
   - The dashboard will load with real-time stock data

## 📊 Dashboard Sections

### 1. Portfolio Overview Tab
- **Portfolio Statistics**: Total value, returns, and performance metrics
- **Performance Chart**: Visual representation of portfolio growth
- **Top Stocks Table**: Best-performing stocks with trading signals

### 2. Individual Stocks Tab
- **Stock Selection**: Dropdown to choose any Sensex 30 stock
- **Price Analysis**: Initial price, current price, and returns
- **Trading Signals**: Current BUY/SELL/HOLD recommendations
- **Price Chart**: Historical price movement visualization

### 3. Strategy Comparison Tab
- **Strategy Performance**: 3-strategy approach vs buy-and-hold
- **Return Comparison**: Side-by-side performance metrics
- **Comparison Chart**: Bar chart showing relative performance

## 🔧 Configuration

### Analysis Periods
- 1 Month
- 3 Months
- 6 Months (default)
- 1 Year
- 2 Years

### Initial Investment
- Default: ₹20,00,000 (20 Lakhs)
- Configurable in `simulate.py`

## 📈 API Endpoints

- `GET /` - Main dashboard page
- `GET /api/portfolio-overview?period=<period>` - Portfolio performance data
- `GET /api/stock-analysis?symbol=<symbol>&period=<period>` - Individual stock analysis
- `GET /api/strategy-comparison?period=<period>` - Strategy comparison data

## 🎨 Features

### Interactive UI
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Tab Navigation**: Easy switching between different views
- **Real-time Updates**: Refresh data with one click
- **Color-coded Signals**: Green for positive, red for negative performance

### Data Visualization
- **Line Charts**: Portfolio and stock price trends
- **Bar Charts**: Strategy comparison
- **Interactive Tables**: Sortable stock performance data
- **Signal Badges**: Visual trading recommendations

## ⚠️ Important Notes

1. **Data Source**: Uses Yahoo Finance API for real-time stock data
2. **Internet Required**: Active internet connection needed for data fetching
3. **Historical Data**: Limited by available historical data from Yahoo Finance
4. **Strategy Limitations**: Past performance doesn't guarantee future results
5. **Investment Disclaimer**: This is for educational purposes only

## 🔄 Updates & Maintenance

### Regular Updates
- Stock data updates automatically when refreshed
- Portfolio calculations are real-time
- Strategy signals update based on latest data

### Data Persistence
- Portfolio data stored in JSON format
- Transaction history maintained
- Performance metrics calculated on-demand

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please consult financial advisors before making real investment decisions.

## 📞 Support

For issues or questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

---

**Disclaimer**: This dashboard is for educational and demonstration purposes only. It should not be used as the sole basis for investment decisions. Always consult with qualified financial advisors before making investment decisions.

