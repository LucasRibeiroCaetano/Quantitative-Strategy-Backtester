# data.py

import yfinance as yf
import pandas as pd

def get_data(symbol, start, end):
    """
    Downloads data and calculates 'Buy & Hold' (Cumulative_Market) return.
    """
    
    # This line remains the same. auto_adjust=True is now default.
    data = yf.download(symbol, start=start, end=end)
    
    if data.empty:
        print(f"No data found for {symbol} in the specified period.")
        return pd.DataFrame()

    # --- THIS IS THE FIX ---
    # Change "Adj Close" to "Close"
    # The 'Close' column IS the adjusted close now.
    data["Market_Return"] = data["Close"].pct_change().fillna(0)
    # -----------------------
    
    data["Cumulative_Market"] = (1 + data["Market_Return"]).cumprod()
    
    return data