import requests
from datetime import timedelta
import yahoo_fin.stock_info as si
import pandas_market_calendars as mcal
from db_helper import query_table
from sql_queries import query_existing_data_for_ticker
from settings import API_KEY, STARTDATE_HISTORY_DATA


def get_dowjones_tickers():

    dow_list = si.tickers_dow()

    return dow_list


def get_trading_days_within_date_range(start_date, end_date):

    nyse = mcal.get_calendar('NYSE')
    days_as_datetime = nyse.valid_days(
        start_date=start_date, end_date=end_date
    ).sort_values()

    days_as_string = [day.strftime('%Y-%m-%d') for day in days_as_datetime]

    return days_as_string


def get_last_business_day(today_date):

    if today_date.weekday() == 0:
        diff = 3
    elif today_date.weekday() == 6:
        diff = 2
    else:
        diff = 1

    result = today_date - timedelta(days=diff)

    return result.strftime('%Y-%m-%d')


def get_missing_dates_for_data_ticker(ticker, today_date):

    missing_dates = list()
    existing_dates = query_table(query_existing_data_for_ticker(ticker))['date'].to_list()
    trading_days = get_trading_days_within_date_range(STARTDATE_HISTORY_DATA, get_last_business_day(today_date))

    for date in trading_days:
        if date not in existing_dates:
            missing_dates.append(date)

    return missing_dates


def get_ticker_price_data(ticker, date):

    url = f"http://api.marketstack.com/v1/eod/{date}?access_key={API_KEY}&symbols={ticker}"

    request = requests.get(url)
    status_code = request.status_code
    if status_code == 200:
        data = request.json()['data'][0]
        return data
    else:
        error_msg = request['text']
        raise Exception(error_msg)
