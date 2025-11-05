import numpy as np

def calculate_metrics(df):
    df = df.dropna().copy()
    returns = df["Strategy_Return"]

    # === Core returns ===
    total_return = df["Cumulative_Strategy"].iloc[-1] - 1
    cagr = (df["Cumulative_Strategy"].iloc[-1]) ** (252 / len(df)) - 1  # Compound Annual Growth Rate

    # === Ratios ===
    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std()
    sortino_ratio = np.sqrt(252) * returns.mean() / downside_std if downside_std != 0 else np.nan

    # === Drawdowns & Calmar ===
    cummax = df["Cumulative_Strategy"].cummax()
    drawdown = (df["Cumulative_Strategy"] - cummax) / cummax
    max_drawdown = drawdown.min()
    calmar_ratio = cagr / abs(max_drawdown) if max_drawdown != 0 else np.nan

    # === Trade-level Profit Factor and Win Rate ===
    df["position_held"] = df["Signal"].shift(1).fillna(0)
    df["trade_change"] = (df["position_held"] != df["position_held"].shift(1)).astype(int)
    df["trade_id"] = df["trade_change"].cumsum()

    trade_returns = df.groupby("trade_id").apply(
        lambda g: (1 + g["Strategy_Return"]).prod() - 1
    )

    trade_pos = df.groupby("trade_id")["position_held"].first()
    trade_returns = trade_returns[trade_pos != 0]  # ignore flat periods

    # --- ADDED METRIC ---
    total_trades = len(trade_returns)
    # --------------------

    gains = trade_returns[trade_returns > 0].sum()
    losses = abs(trade_returns[trade_returns < 0].sum())
    profit_factor = gains / losses if losses != 0 else np.nan
    win_rate = len(trade_returns[trade_returns > 0]) / len(trade_returns) if len(trade_returns) > 0 else np.nan

    # Clean up helper columns
    df.drop(columns=["position_held", "trade_change", "trade_id"], inplace=True, errors="ignore")

    # === Results dictionary ===
    metrics = {
        "Total Return": f"{total_return*100:.2f}%",
        "CAGR": f"{cagr*100:.2f}%",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Sortino Ratio": f"{sortino_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown*100:.2f}%",
        "Calmar Ratio": f"{calmar_ratio:.2f}",
        "Total Trades": total_trades,  # <-- ADDED HERE
        "Profit Factor": f"{profit_factor:.2f}" if not np.isnan(profit_factor) else "NaN",
        "Win Rate": f"{win_rate*100:.2f}%"
    }

    return metrics