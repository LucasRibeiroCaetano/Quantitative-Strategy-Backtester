import matplotlib.pyplot as plt

def plot_results(data, metrics):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10,6))
    fig.canvas.manager.set_window_title("Strategy Backtesting")

    ax.plot(data["Cumulative_Market"], label="Market (Buy & Hold)")
    ax.plot(data["Cumulative_Strategy"], label="Strategy SMA 20/50")
    ax.set_title("Moving Average Crossover Strategy vs Market")
    ax.set_xlabel("Data")
    ax.set_ylabel("Cumulative Returns")
    ax.legend()
    ax.grid(True)

    # Métricas
    text_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
    plt.subplots_adjust(right=0.75)
    fig.text(
        0.77, 0.5, text_str,
        fontsize=9, va='center',
        bbox=dict(facecolor="#222222", alpha=0.8, boxstyle='round,pad=0.5')
    )

    plt.show()