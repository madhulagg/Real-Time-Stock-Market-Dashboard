def sma_crossover(prices):
    dates = list(prices.keys())
    closes = list(prices.values())
    signals = {}
    for i in range(10, len(closes)):
        short_sma = sum(closes[i-5:i]) / 5
        long_sma = sum(closes[i-10:i]) / 10
        signals[dates[i]] = "BUY" if short_sma > long_sma else "SELL" if short_sma < long_sma else "HOLD"
    return signals

def momentum_strategy(prices):
    dates = list(prices.keys())
    closes = list(prices.values())
    signals = {}
    for i in range(10, len(closes)):
        diff = closes[i] - closes[i-10]
        signals[dates[i]] = "BUY" if diff > 0 else "SELL" if diff < 0 else "HOLD"
    return signals

def rsi_strategy(prices):
    dates = list(prices.keys())
    closes = list(prices.values())
    signals = {}
    for i in range(14, len(closes)):
        gains = [closes[j] - closes[j-1] for j in range(i-13, i+1) if closes[j] > closes[j-1]]
        losses = [-1 * (closes[j] - closes[j-1]) for j in range(i-13, i+1) if closes[j] < closes[j-1]]
        avg_gain = sum(gains) / 14 if gains else 0
        avg_loss = sum(losses) / 14 if losses else 0
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi = 100 - (100 / (1 + rs))
        signals[dates[i]] = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
    return signals
