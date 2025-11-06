import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotx

def plot_results(data, metrics, symbol):
    
    plt.style.use(matplotx.styles.nord)

    # --- 1. Create a Figure and a GridSpec for a dashboard layout ---
    # We create a wider, shorter figure
    fig = plt.figure(figsize=(16, 10)) 
    
    # Create a 2-row, 2-column grid.
    # The left column (for plots) will be 3x wider than the right (for table)
    gs = fig.add_gridspec(
        nrows=2, 
        ncols=2, 
        width_ratios=[3, 1], 
        height_ratios=[1, 1]
    )
    # -----------------------------------------------------------------

    fig.canvas.manager.set_window_title(f"Strategy Backtesting: {symbol}")

    # --- 2. Define the subplots on the grid ---
    ax1 = fig.add_subplot(gs[0, 0])      # Row 0, Col 0 (Returns)
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1) # Row 1, Col 0 (Drawdown)
    ax_table = fig.add_subplot(gs[:, 1])   # All Rows, Col 1 (Table)
    
    # Hide x-tick labels on ax1 (top plot)
    plt.setp(ax1.get_xticklabels(), visible=False) 
    # -------------------------------------------
    
    # --- PLOT 1: Cumulative Returns (on 'ax1') ---
    ax1.plot(data["Cumulative_Market"], label=f"{symbol} Market (Buy & Hold)")    
    ax1.plot(data["Cumulative_Strategy"], label=f"{symbol} Strategy")
    
    if "Benchmark_SP500" in data.columns:
        ax1.plot(
            data["Benchmark_SP500"], 
            label="S&P 500 Benchmark", 
            linestyle='--'
        )

    ax1.set_title("Cumulative Returns")
    ax1.set_ylabel("Cumulative Returns")
    ax1.grid(True)
    matplotx.line_labels(ax1)

    # --- PLOT 2: Drawdown Time-Series (on 'ax2') ---
    cummax = data["Cumulative_Strategy"].cummax()
    drawdown = (data["Cumulative_Strategy"] - cummax) / cummax
    
    ax2.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    ax2.set_title("Strategy Drawdown")
    ax2.set_ylabel("Drawdown")
    ax2.set_xlabel("Date")
    ax2.grid(True)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # --- PLOT 3: Metrics Table (on 'ax_table') ---
    ax_table.axis('off') 
    metrics_list = list(metrics.items())
    
    table = ax_table.table(
        cellText=metrics_list,
        colLabels=["Metric", "Value"],
        loc='center',
        cellLoc='left',
        colWidths=[0.6, 0.4] # 60%/40% split within the table's column
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    
    # --- 3. Scale table to fit the new vertical slot ---
    # We set width to 1.0 (100% of its column)
    # We set height to 1.8 to give the 9 rows more space
    table.scale(1.0, 1.8)
    # -------------------------------------------------

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('none')
        if (row == 0): 
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#3B4252') # Nord header color
        else:
            cell.set_facecolor('#2E3440') # Nord background color

    # Use tight_layout to make everything fit nicely
    plt.tight_layout(pad=2.0)
    plt.show()