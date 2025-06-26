def sma_crossover(prices, short_window = 5, long_window = 15):
    dates = list(prices.keys())
    values = list(prices.values())
    signals = []

    for i in range(len(values)):
        if i < long_window:
            signals.append("HOLD")
            continue
        short_avg = sum(values[i - short_window:i])/short_window
        long_avg = sum(values[i - long_window:i])/long_window
        if short_avg > long_avg:
            signals.append("BUY")
        elif short_avg < long_avg:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return dict(zip(dates, signals))

def simple_rsi(prices, period=14):
    dates = list(prices.keys())
    values = list(prices.values())
    signals = []

    for i in range(len(values)):
        if i < period:
            signals.append("HOLD")
            continue
        gains = 0
        losses = 0
        for j in range(i - period + 1, i + 1):
            diff = values[j] - values[j - 1]
            if diff > 0:
                gains += diff
            else:
                losses -= diff
        if losses == 0:
            rsi = 100
        else:
            rs = gains / losses
            rsi = 100 - (100 / (1 + rs))

        if rsi < 30:
            signals.append("BUY")
        elif rsi > 70:
            signals.append("SELL")
        else:
            signals.append("HOLD")

    return dict(zip(dates, signals))


def mean_reversion(prices, window=20, threshold=0.05):
    dates = list(prices.keys())
    values = list(prices.values())
    signals = []

    for i in range(len(values)):
        if i < window:
            signals.append("HOLD")
            continue
        avg = sum(values[i - window:i]) / window
        price = values[i]
        if (avg - price) / avg > threshold:
            signals.append("BUY")
        elif (price - avg) / avg > threshold:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return dict(zip(dates, signals))


def generate_signals(prices, strategy_name):
    if strategy_name == "sma":
        return sma_crossover(prices)
    elif strategy_name == "rsi":
        return simple_rsi(prices)
    elif strategy_name == "mean":
        return mean_reversion(prices)
    else:
        raise ValueError("Unknown strategy selected.")