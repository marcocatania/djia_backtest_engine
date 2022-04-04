from db_helper import query_table, sql_execute
from sql_queries import query_open_positions, \
    query_existing_data_for_ticker, log_buy_position, \
    query_existing_portfolio_entry, query_log_portfolio_data, \
    log_sell_position
from api_helper import get_dowjones_tickers, \
    get_trading_days_within_date_range
from Ticker import Ticker
from datetime import datetime, timedelta
from settings import OPENING_BALANCE, \
    MAX_POSITION_SIZE, STARTDATE_BACKTEST, \
    TRANSACTION_COST
import copy


class StrategyPrice2DaysUp:

    def __init__(self, trading_date):
        self.trading_date = trading_date
        if self.trading_date == STARTDATE_BACKTEST:
            # Default values
            self.cash = OPENING_BALANCE
            self.positions_size = 0
            self.portfolio_size = OPENING_BALANCE
            self.portfolio_size_previous_day = OPENING_BALANCE
            self.pnl_previous_day = 0
        else:
            self.previous_day = get_trading_days_within_date_range(
                STARTDATE_BACKTEST, datetime.strptime(self.trading_date, '%Y-%m-%d')
            )[-2]
            portfolio_previous_day_data = query_table(
                query_existing_portfolio_entry(self.previous_day)
            )

            self.cash = portfolio_previous_day_data.iloc[0]['cash_value']
            self.positions_size = portfolio_previous_day_data.iloc[0]['positions_value']
            self.pnl_previous_day = portfolio_previous_day_data.iloc[0]['pnl']
            self.portfolio_size_previous_day = copy.deepcopy(self.cash) + copy.deepcopy(self.positions_size)
            self.portfolio_size = self.cash + self.positions_size
        # Get stocks to sell today
        self.stocks_to_sell = self.select_today_stocks_to_sell()
        # Get stocks to buy today
        self.stocks_to_buy = self.select_today_stocks_to_buy()

        self.execute_sell_orders()
        self.execute_buy_orders()

        self.update_portfolio()

    def update_portfolio(self):

        porfolio_value_today = self.positions_size + self.cash
        overall_pnl = porfolio_value_today - OPENING_BALANCE

        if self.positions_size < 0:
            self.cash += self.positions_size
            self.positions_size = 0

        sql_execute(
            query_log_portfolio_data(
                self.trading_date,
                self.positions_size,
                self.cash,
                overall_pnl
            )
        )

    def execute_buy_orders(self):

        for ticker in self.stocks_to_buy:

            ticker_data = query_table(query_existing_data_for_ticker(ticker))
            price_stock = ticker_data.loc[ticker_data['date'] == self.trading_date].iloc[0]['adj_close']
            max_position_value = self.portfolio_size * MAX_POSITION_SIZE
            total_price_stock = price_stock * (1+TRANSACTION_COST)
            num_shares_to_buy = int(max_position_value / total_price_stock)
            total_cost_position = num_shares_to_buy * total_price_stock
            if (total_cost_position > self.cash) or (num_shares_to_buy == 0):
                break
            sql_execute(
                log_buy_position(
                    ticker,
                    total_price_stock,
                    self.trading_date,
                    num_shares_to_buy
                ))
            self.cash = self.cash - total_cost_position
            self.positions_size += price_stock * num_shares_to_buy

    def execute_sell_orders(self):

        for ticker in self.stocks_to_sell:
            ticker_data = query_table(query_existing_data_for_ticker(ticker))
            price_stock = ticker_data.loc[ticker_data['date'] == self.trading_date].iloc[0]['adj_close']
            position_data = query_table(query_open_positions())
            position_size = position_data.loc[ticker_data['ticker'] == ticker].iloc[0]['count_shares']
            initial_cost_per_share = position_data.loc[ticker_data['ticker'] == ticker].iloc[0]['cost_per_share']
            initial_position_cost = position_size * initial_cost_per_share
            value_order = position_size * price_stock
            cash_in = value_order - (value_order * TRANSACTION_COST)

            self.cash += cash_in
            self.positions_size -= initial_position_cost

            sql_execute(
                log_sell_position(
                    ticker,
                    self.trading_date
            ))

    def select_today_stocks_to_buy(self):

        dowjones_tickers = get_dowjones_tickers()

        ticker_last_3_trading_days = self.get_ticker_last_3_trading_days()

        analysis_dates = ticker_last_3_trading_days[:2]

        result = list()

        for _ in dowjones_tickers:
            if _ not in self.stocks_to_sell:

                ticker = Ticker(_)

                ticker_data = ticker.get_ticker_history_data()

                analysis_data = ticker_data[ticker_data['date'].isin(analysis_dates)]

                two_consecutive_days_up = analysis_data.iloc[1]['adj_close'] > analysis_data.iloc[0]['adj_close']

                if two_consecutive_days_up:
                    diff = 1 - (
                            analysis_data.iloc[0]['adj_close']/analysis_data.iloc[1]['adj_close']
                    )
                    result.append((_, diff))

        result = sorted(result, key=lambda x: x[1], reverse=True)

        return [i[0] for i in result]

    def select_today_stocks_to_sell(self):

        ticker_positions = query_table(
            query_open_positions()
        )['ticker'].to_list()

        return ticker_positions

    def get_ticker_last_3_trading_days(self):
        last_3_trading_days = get_trading_days_within_date_range(
            (datetime.strptime(self.trading_date, '%Y-%m-%d') - timedelta(days=14)).strftime('%Y-%m-%d'),
            self.trading_date
        )[-3:]

        return last_3_trading_days

    @staticmethod
    def get_trading_days_data(ticker_data, trading_days):

        result = ticker_data[ticker_data['date'].isin(trading_days)]

        return result


