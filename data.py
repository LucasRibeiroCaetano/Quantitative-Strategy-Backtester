import yfinance as yf

def get_data(symbol, start, end, interval="1d"):
    data = yf.download(symbol, start=start, end=end, interval=interval)
    data.dropna(inplace=True)
    return data