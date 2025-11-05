import argparse
from data import get_data
from strategy import sma_crossover
from metrics import calculate_metrics
from plots import plot_results

def main():
    parser = argparse.ArgumentParser(description="Strategy Backtester")
    parser.add_argument("--symbol", type=str, required=True, help="Ticker do ativo (ex: AAPL, BTC-USD, EURUSD=X)")
    parser.add_argument("--start", type=str, default="2020-01-01", help="Data inicial (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-12-31", help="Data final (YYYY-MM-DD)")
    args = parser.parse_args()

    data = get_data(args.symbol, args.start, args.end)
    data = sma_crossover(data)
    metrics = calculate_metrics(data)

    print("\nStrategy Performance Metrics\n")
    for key, value in metrics.items():
        print(f"{key:20s}: {value}")

    plot_results(data, metrics)

if __name__ == "__main__":
    main()
