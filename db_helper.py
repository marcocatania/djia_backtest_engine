import sqlite3
import pandas as pd
import os
import settings
import sql_queries


def connect_db():
    """
    Set db file path and create connection
    :return: db connection
    """
    db_path = settings.DB_LOCATION if \
        (settings.DB_LOCATION != "" and os.path.exists(settings.DB_LOCATION)) \
        else os.getcwd()

    db_name = settings.DB_NAME if \
        settings.DB_NAME != "" \
        else "default.db"

    conn_parameter = db_path + "/" + db_name

    conn = None

    try:
        conn = sqlite3.connect(conn_parameter)
        return conn
    except Exception as e:
        print(e)

    return conn


def sql_execute(sql_statement):
    """
    Create a table in SQLite executing SQL statement
    :param sql_statement: SQL statement string
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.rollback()
        conn.close()


def query_table(sql_query):
    """
    Query a table in SQLite executing SQL statement
    :param sql_query: SQL statement to execute
    """
    try:
        conn = connect_db()
        data = pd.read_sql_query(sql_query, conn)
        return data
    except Exception as e:
        raise e
    finally:
        conn.close()


def initialise_schema():
    """
    Create DB tables if not existing
    """
    try:
        sql_execute(sql_queries.query_create_ticker_data_table())
        sql_execute("DROP TABLE IF EXISTS positions;")
        sql_execute("DROP TABLE IF EXISTS portfolio;")
        sql_execute(sql_queries.query_create_positions_table())
        sql_execute(sql_queries.query_create_portfolio_table())

    except Exception as e:
        raise e
