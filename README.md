# DJIA Stocks Backtest Engine

Uses stock eod quotes from MarketStack 
to run backtest on DJIA stocks.

Universe: DJIA index.

Tool has been make flexible for user to simulate real market conditions
(max position size, transaction cost and other can be modified).
Otuput is an excel file with portfolio performance and positions over time.

## Strategy

 For each trading day:

App loos back for data of last 3 trading days.

Most recent date is used to execute trade.

2 others days are used for analysis and decide trades.

Trade: for each stock, if price has been rising for 2 consecutive days,
    we place a buy order.

All  positions are closed following business day.

We only buy stocks members of DJIA and that we didn't hold overnight.


## Requirements

* Python 3.10
* [PIP modules] - Use requirements.txt to install required

## Installation

How to install required modules

    pip install requirements.txt

## How to run application

    python main.py

