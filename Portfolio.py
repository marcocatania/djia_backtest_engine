from settings import STARTDATE_BACKTEST
from api_helper import get_last_business_day, \
    get_trading_days_within_date_range
from strategy import StrategyPrice2DaysUp


class Portfolio:

    def __init__(self, today_date):
        self.today_date = today_date
        # Get all trading days between date start backtest and yesterday
        self.trading_days = get_trading_days_within_date_range(
            STARTDATE_BACKTEST,
            get_last_business_day(self.today_date)
        )
        self.create_positions()

    def create_positions(self):

        # Run backtest for each trading day
        for trading_day in self.trading_days:
            StrategyPrice2DaysUp(trading_day)
