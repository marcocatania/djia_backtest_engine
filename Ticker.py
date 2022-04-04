from api_helper import get_ticker_price_data, \
    get_missing_dates_for_data_ticker
from db_helper import sql_execute, query_table
from sql_queries import query_insert_ticker_data, query_ticker_data
from datetime import datetime


class Ticker:

    def __init__(self, symbol):
        self.ticker = symbol
        self.today_date = datetime.now().date()

    def initialize_ticker_data(self):

        trading_dates_to_get_data = get_missing_dates_for_data_ticker(self.ticker, self.today_date)

        for date in trading_dates_to_get_data:
            # Populate in DB history eod price for all tickers
            try:
                data_api = get_ticker_price_data(ticker=self.ticker, date=date)
            except Exception as e:
                print(e)
                continue
            query_insert_data = query_insert_ticker_data(
                data_api['symbol'],
                data_api['exchange'],
                data_api['open'],
                data_api['high'],
                data_api['low'],
                data_api['close'],
                data_api['volume'],
                data_api['adj_high'],
                data_api['adj_low'],
                data_api['adj_close'],
                data_api['adj_open'],
                data_api['adj_volume'],
                data_api['split_factor'],
                data_api['dividend'],
                datetime.strptime(data_api['date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')
            )
            try:
                sql_execute(query_insert_data)
            except Exception as e:
                print(e)

    def get_ticker_history_data(self):

        data = query_table(query_ticker_data(self.ticker))

        return data









