from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime, timedelta 
from alpaca_trade_api import REST
from finbert_utils import estimate_sentiment


API_KEY = "your-alpaca-api-key"
API_SECRET = "your-alpaca-secret-key"
BASE_URL = "your-alpaca-base-url"

ALPACA_CREDS = {
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
    'PAPER': True
}


class MLTrader(Strategy):
    def initialize(self, symbol:str='SPY', cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = '24H'
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
    
    
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity
        
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        news = [ev.__dict__['_raw']['headline'] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment
        


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()
        
        if cash > last_price:
            if sentiment == 'positive' and probability > .999:
                if self.last_trade == 'sell':
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    'buy',
                    type='bracket',
                    take_profit=last_price * 1.20, # Take profit at 20% above the last price
                    stop_loss=last_price * 0.95, # Stop loss at 5% below the last price
                )
                self.submit_order(order)
                self.last_trade = 'buy'
            
            
            elif sentiment == 'negative' and probability > .999:
                if self.last_trade == 'buy':
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    'sell',
                    type='bracket',
                    take_profit=last_price * .8, # Take profit at 20% above the last price
                    stop_loss=last_price * 1.05, # Stop loss at 5% below the last price
                )
                self.submit_order(order)
                self.last_trade = 'sell'
    
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)


broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker, 
                    parameters={'symbol':'SPY', 
                                'cash_at_risk':.5})
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={'symbol':'SPY', 
                'cash_at_risk':.5}
)

# If you want to deploy the bot
# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()
