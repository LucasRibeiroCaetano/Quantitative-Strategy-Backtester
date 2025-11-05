import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Obter dados históricos
data = yf.download("AAPL", start="2020-01-01", end="2024-12-31", interval="1d")
data.dropna(inplace=True)

# Criar indicadores e sinais
data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["SMA_50"] = data["Close"].rolling(window=50).mean()

# Sinal: 1 = comprar, -1 = vender
data["Signal"] = np.where(data["SMA_20"] > data["SMA_50"], 1, -1)

# Calcular retornos
data["Return"] = data["Close"].pct_change()
data["Strategy_Return"] = data["Signal"].shift(1) * data["Return"]

# Cálculo do crescimento acumulado
data["Cumulative_Market"] = (1 + data["Return"]).cumprod()
data["Cumulative_Strategy"] = (1 + data["Strategy_Return"]).cumprod()

# Métricas de performance
def calculate_metrics(df):
    df = df.dropna().copy()
    returns = df["Strategy_Return"]

    total_return = df["Cumulative_Strategy"].iloc[-1] - 1
    annual_return = (1 + total_return) ** (252 / len(df)) - 1  # 252 dias úteis

    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
    
    cummax = df["Cumulative_Strategy"].cummax()
    drawdown = (df["Cumulative_Strategy"] - cummax) / cummax
    max_drawdown = drawdown.min()

    # Profit factor: soma dos ganhos / soma das perdas
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

metrics = calculate_metrics(data)

# Mostrar resultados na consola
print("Strategy Performance Metrics\n")
for key, value in metrics.items():
    print(f"{key:20s}: {value}")

# Gráfico comparativo
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(data["Cumulative_Market"], label="Market (Buy & Hold)")
ax.plot(data["Cumulative_Strategy"], label="Strategy SMA 20/50")
ax.set_title("Moving Average Crossover Strategy vs Market")
ax.set_xlabel("Data")
ax.set_ylabel("Cumulative Returns")
ax.legend()
ax.grid(True)

# === Adicionar métricas fora do gráfico ===
text_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
plt.subplots_adjust(right=0.75)  # cria espaço extra à direita
fig.text(
    0.77, 0.5, text_str,
    fontsize=9, va='center',
    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5')
)

plt.show()
