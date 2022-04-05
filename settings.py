"""
constants used as parameters for application
"""

# Do not change to avoid regenerating DB (API calls)
DB_LOCATION = ""  # path db file
DB_NAME = ""  # custom DB name (ie database.db)

# API
API_KEY = "" # Add API key

# Backtesting
STARTDATE_HISTORY_DATA = '2022-02-25'
STARTDATE_BACKTEST = '2022-03-01'
MAX_POSITION_SIZE = 0.1  # Share of portfolio (0.1 as 10%)
OPENING_BALANCE = 10000  # USD
TRANSACTION_COST = 0.0001  # bps in decimal form
