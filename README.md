# Strategy Backtester

This is a simple, command-line based backtesting tool built in Python. It downloads historical financial data, applies a trading strategy (currently a Simple Moving Average crossover as sample), calculates key performance metrics, and plots the cumulative returns and drawdown.

## Features

* Fetches data for any ticker available on Yahoo Finance (stocks, crypto, forex).
* Calculates a wide range of performance metrics:
    * Total Return & CAGR
    * Sharpe & Sortino Ratios
    * Max Drawdown & Calmar Ratio
    * Total Trades, Win Rate, & Profit Factor
* Plots strategy performance against a "Buy & Hold" benchmark.
* Displays a time-series graph of strategy drawdowns.

## Requirements

To run this project, you will need Python 3.x and the following libraries:

* **pandas**: For data manipulation and analysis.
* **numpy**: For numerical calculations.
* **matplotlib**: For generating plots.
* **matplotx**: Matplotlib themes.
* **yfinance**: For downloading historical market data.

### Installation

You can install all dependencies at once using `pip`:

```bash
pip install pandas numpy matplotlib yfinance matplotx
```

### How to Use
The script is run from the command line using main.py. You must provide a ticker symbol and can optionally specify a start and end date.

### Command-Line Arguments
--symbol (Required): The ticker symbol to backtest (e.g., AAPL, BTC-USD, EURUSD=X).

--start (Optional): The start date for the backtest in YYYY-MM-DD format. (Default: 2020-01-01)

--end (Optional): The end date for the backtest in YYYY-MM-DD format. (Default: 2024-12-31)

### Example
To run a backtest for Apple (AAPL) from the beginning of 2020 to the present:

```bash
python main.py --symbol AAPL --start 2020-01-01
```
To run a backtest for Bitcoin (BTC-USD) for the year 2023:

```bash
python main.py --symbol BTC-USD --start 2023-01-01 --end 2023-12-31
```

The script will execute the backtest and then display a plot window titled "Strategy Backtesting" with the results.
