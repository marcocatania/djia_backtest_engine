import sys
import os
from datetime import datetime
import numpy as np
from db_helper import initialise_schema, query_table
from api_helper import get_dowjones_tickers
from sql_queries import query_open_positions
from Ticker import Ticker
from Portfolio import Portfolio
from report import write_portfolio_details
from settings import API_KEY, STARTDATE_BACKTEST, \
    STARTDATE_HISTORY_DATA


if __name__ == "__main__":
    
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    today_date = datetime.now().date()

    if len(API_KEY) == 0:
        sys.exit("Please add to settings an API key")

    startdate_history_data_dt = datetime.strptime(
        STARTDATE_HISTORY_DATA, '%Y-%m-%d')
    startdate_backtest_data_dt = datetime.strptime(
        STARTDATE_BACKTEST, '%Y-%m-%d')
    delta = np.busday_count(
        STARTDATE_HISTORY_DATA, STARTDATE_BACKTEST)
    if delta < 2:
        sys.exit(
            "Error: You should have at least 2 days "
            "between start history and backtest")

    try:
        initialise_schema()
        print()
        print("Retrieving DJIA tickers...")
        dowjones_tickers = get_dowjones_tickers()
    except Exception as e:
        sys.exit(e)

    print()
    print("Retrieving tickers data...")
    symbol_open_positions = query_table(query_open_positions())['ticker'].to_list()
    all_tickers = set(dowjones_tickers + symbol_open_positions)
    for symbol in all_tickers:
        ticker = Ticker(symbol)
        ticker.initialize_ticker_data()

    print()
    print("Running backtest...")
    Portfolio(today_date)

    report_name = f"report_{today_date.strftime('%Y-%m-%d')}.xlsx"

    print()
    print(f"Saving report as {report_name}")
    write_portfolio_details(report_name)
