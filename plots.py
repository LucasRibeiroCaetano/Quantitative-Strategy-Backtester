# plots.py

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # Make sure this import is here

def plot_results(data, metrics, symbol):
    
    plt.style.use('dark_background')

    # Creates 2 charts (ax1, ax2) stacked vertically
    fig, (ax1, ax2) = plt.subplots(
        nrows=2, 
        ncols=1, 
        figsize=(10, 12),
        sharex=True
    )
    
    fig.canvas.manager.set_window_title("Strategy Backtesting")

    # --- PLOT 1: Cumulative Returns (on 'ax1') ---
    
    # Plot 1: Market (Buy & Hold of your asset)
    ax1.plot(data["Cumulative_Market"], label=f"{symbol} Market (Buy & Hold)")    
    # Plot 2: Strategy
    ax1.plot(data["Cumulative_Strategy"], label=f"{symbol} Strategy")
    # Plot 3: Benchmark (S&P 500)
    # This 'if' statement checks if main.py successfully added the column
    if "Benchmark_SP500" in data.columns:
        ax1.plot(
            data["Benchmark_SP500"], 
            label="S&P 500 Benchmark", 
            color='red'
        )
    # ------------------

    ax1.set_title("Cumulative Returns") # <-- This is the new title
    ax1.set_ylabel("Cumulative Returns")
    ax1.legend() # The legend will now show all 3
    ax1.grid(True)

    # --- PLOT 2: Drawdown Time-Series (on 'ax2') ---
    cummax = data["Cumulative_Strategy"].cummax()
    drawdown = (data["Cumulative_Strategy"] - cummax) / cummax
    
    ax2.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    ax2.set_title("Strategy Drawdown")
    ax2.set_ylabel("Drawdown")
    ax2.set_xlabel("Date")
    ax2.grid(True)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # Add metrics text box (as before)
    text_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
    plt.subplots_adjust(right=0.75, top=0.95, bottom=0.05) 
    
    fig.text(
        0.77, 0.5, text_str,
        fontsize=9, va='center',
        bbox=dict(facecolor='#222222', alpha=0.8, boxstyle='round,pad=0.5')
    )

    plt.show()