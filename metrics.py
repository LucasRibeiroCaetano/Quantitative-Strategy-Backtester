import numpy as np

def calculate_metrics(df):
    df = df.dropna().copy()
    returns = df["Strategy_Return"]

    total_return = df["Cumulative_Strategy"].iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(df)) - 1  # 252 dias úteis

    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
    cummax = df["Cumulative_Strategy"].cummax()
    drawdown = (df["Cumulative_Strategy"] - cummax) / cummax
    max_drawdown = drawdown.min()

    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    profit_factor = gains / losses if losses != 0 else np.nan

    win_rate = len(returns[returns > 0]) / len(returns)

    metrics = {
        "Total Return": f"{total_return*100:.2f}%",
        "Annualized Return": f"{annual_return*100:.2f}%",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown*100:.2f}%",
        "Profit Factor": f"{profit_factor:.2f}",
        "Win Rate": f"{win_rate*100:.2f}%"
    }

    return metrics
