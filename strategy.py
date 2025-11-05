import numpy as np

def sma_crossover(data, short_window=20, long_window=50):
    data["SMA_20"] = data["Close"].rolling(window=short_window).mean()
    data["SMA_50"] = data["Close"].rolling(window=long_window).mean()

    data["Signal"] = np.where(data["SMA_20"] > data["SMA_50"], 1, -1)
    data["Return"] = data["Close"].pct_change()
    data["Strategy_Return"] = data["Signal"].shift(1) * data["Return"]

    data["Cumulative_Market"] = (1 + data["Return"]).cumprod()
    data["Cumulative_Strategy"] = (1 + data["Strategy_Return"]).cumprod()

    return data
