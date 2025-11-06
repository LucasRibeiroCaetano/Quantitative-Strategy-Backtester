# main.py

import argparse
from data import get_data
from strategy import sma_crossover
from metrics import calculate_metrics
from plots import plot_results

def main():
    parser = argparse.ArgumentParser(description="Strategy Backtester")
    parser.add_argument("--symbol", type=str, required=True, help="Asset ticker (e.g., AAPL, BTC-USD, EURUSD=X)")
    parser.add_argument("--start", type=str, default="2020-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-12-31", help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    # 1. Load main asset data
    data = get_data(args.symbol, args.start, args.end)
    if data.empty:
        return # Exit if no data

    # 2. Load Benchmark (S&P 500) data
    print("Loading S&P 500 (^GSPC) benchmark data...")
    benchmark_data = get_data("^GSPC", args.start, args.end)

    # 3. Apply strategy to main asset data
    data = sma_crossover(data)

    # 4. Join benchmark data to main DataFrame
    if not benchmark_data.empty:
        # Rename the column to avoid conflicts and join it
        data["Benchmark_SP500"] = benchmark_data["Cumulative_Market"]
    else:
        print("Warning: Could not load S&P 500 benchmark data.")

    # 5. Calculate metrics (based on the strategy 'data')
    metrics = calculate_metrics(data)

    # 6. Plot results
    # 'data' now contains Cumulative_Market (asset), Cumulative_Strategy, and Benchmark_SP500
    plot_results(data, metrics, args.symbol)

if __name__ == "__main__":
    main()