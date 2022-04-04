"""
This file contains all SQL queries used my app
"""


def query_create_ticker_data_table():

    query = "CREATE TABLE " \
            "IF NOT EXISTS ticker_data (" \
            "ticker TEXT, " \
            "exchange TEXT, " \
            "open REAL,  " \
            "high REAL, " \
            "low REAL, " \
            "close REAL, " \
            "volume INT, " \
            "adj_high REAL, " \
            "adj_low REAL, " \
            "adj_close REAL, " \
            "adj_open REAL, " \
            "adj_volume INT, " \
            "split_factor REAL, " \
            "dividend REAL, " \
            "date TEXT" \
            "); "

    return query


def query_create_positions_table():

    query = "CREATE TABLE " \
            "IF NOT EXISTS positions (" \
            "ticker TEXT, " \
            "cost_per_share REAL, " \
            "open_date TEXT,  " \
            "close_date TEXT, " \
            "count_shares INT" \
            "); "

    return query


def query_portfolio_open_positions_for_date(trading_date):

    query = "SELECT * FROM positions WHERE " \
            f"date(open_date) <= date('{trading_date}') " \
            f"AND date(close_date) >= date('{trading_date}'); "

    return query


def log_buy_position(
        ticker,
        total_price_stock,
        trading_date,
        num_shares_to_buy
):

    query = "INSERT INTO positions " \
        f"VALUES ('{ticker}', " \
        f"'{total_price_stock}', " \
        f"'{trading_date}', " \
        "'2099-12-31', " \
        f"'{num_shares_to_buy}'" \
        ");"

    return query


def log_sell_position(
        ticker,
        trading_date
):
    query = "UPDATE positions " \
        f"SET close_date = '{trading_date}' " \
        f"WHERE ticker = '{ticker}' " \
        "AND close_date = '2099-12-31'" \
        ";"

    return query


def query_create_portfolio_table():

    query = "CREATE TABLE " \
            "IF NOT EXISTS portfolio (" \
            "date TEXT, " \
            "positions_value REAL, " \
            "cash_value REAL,  " \
            "pnl REAL" \
            "); "

    return query


def query_log_portfolio_data(
        trading_date,
        positions_value,
        cash_value,
        pnl
):

    query = "INSERT INTO portfolio " \
            "VALUES (" \
            f"'{trading_date}', " \
            f"'{positions_value}', " \
            f"'{cash_value}',  " \
            f"'{pnl}'" \
            "); "

    return query


def query_insert_ticker_data(ticker,
                             exchange,
                             open,
                             high,
                             low,
                             close,
                             volume,
                             adj_high,
                             adj_low,
                             adj_close,
                             adj_open,
                             adj_volume,
                             split_factor,
                             dividend,
                             date
                             ):

    query = "INSERT INTO ticker_data " \
            "VALUES (" \
            f"'{ticker}', " \
            f"'{exchange}', " \
            f"'{open}', " \
            f"'{high}', " \
            f"'{low}', " \
            f"'{close}', " \
            f"'{volume}', " \
            f"'{adj_high}', " \
            f"'{adj_low}', " \
            f"'{adj_close}', " \
            f"'{adj_open}', " \
            f"'{adj_volume}', " \
            f"'{split_factor}', " \
            f"'{dividend}', " \
            f"'{date}'" \
            ");"

    return query


def query_ticker_data(symbol):

    query = "SELECT " \
            "ticker, " \
            "exchange, " \
            "open, " \
            "high, " \
            "low, " \
            "close, " \
            "volume, " \
            "adj_high, " \
            "adj_low, " \
            "adj_close, " \
            "adj_open, " \
            "adj_volume, " \
            "split_factor, " \
            "dividend, " \
            "date " \
            f"FROM ticker_data WHERE ticker = '{symbol}' " \
            "ORDER BY substr (date,0,4) || substr(date,5,7) || substr(date,8,10)"

    return query


def query_existing_data_for_ticker(symbol):

    query = "SELECT * " \
        f"FROM ticker_data WHERE ticker = '{symbol}'"

    return query


def query_open_positions():

    query = "SELECT * " \
        "FROM positions WHERE " \
        "close_date = '2099-12-31'"

    return query


def query_existing_portfolio_entry(date):

    query = f"SELECT * FROM portfolio where date = '{date}'"

    return query
