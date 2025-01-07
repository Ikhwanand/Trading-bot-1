# Trading-bot-1

## Overview
Trading-bot-1 is a Python project that utilizes the Alpaca API to trade stocks based on sentiment analysis. The project uses the FinBERT model for sentiment analysis and the backtrader library for backtesting strategies.

## Files

### finbert_utils.py
This script is responsible for sentiment analysis. It uses the FinBERT model to estimate the sentiment of given news headlines.

### tradingbot.py
This is the main script of the project. It contains the `MLTrader` class, which is a subclass of `backtrader.Strategy`. The class implements a trading strategy based on sentiment analysis.

## How to Use

1. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```
2. Run the `tradingbot.py` script to start the trading bot.

## Configuration

The following constants need to be set in the `tradingbot.py` script:

- `API_KEY`: Your Alpaca API key.
- `API_SECRET`: Your Alpaca API secret.
- `ALPACA_CREDS`: A dictionary containing your Alpaca API credentials.
- `BASE_URL`: The base URL for the Alpaca API.

## Trading Strategy

The `MLTrader` class implements the following methods:

- `initialize()`: Initializes the trading strategy.
- `position_sizing()`: Determines the size of the position to take.
- `get_dates()`: Gets the current date and the date three days prior.
- `get_sentiment()`: Gets the sentiment of the news headlines for the given symbol.
- `on_trading_iteration()`: This method is called on every trading iteration. It checks the sentiment and makes a trade if the conditions are met.

## Backtesting

To backtest the strategy, you can use the `backtest()` method of the `MLTrader` class. This method takes the following parameters:

- `data_feeder`: An instance of a class that feeds data to the strategy.
- `start_date`: The start date for the backtest.
- `end_date`: The end date for the backtest.
- `parameters`: A dictionary containing the parameters for the strategy.

## Note

Please ensure that you have the necessary permissions and understand the risks before using this trading bot. The authors of this project are not responsible for any losses incurred while using this bot. The python version less or equal than 3.11 is recommended.