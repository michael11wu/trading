from alpaca.data.requests import StockBarsRequest, StockQuotesRequest, StockTradesRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta

from trading_client import orderStock, sellStock
import main

import numpy
import matplotlib.pyplot as plt
from time import sleep

def movingDayAverage(day_interval, ticker):
    #Setting up bar requests
    stock_bars_request = StockBarsRequest(
                                symbol_or_symbols= ticker, 
                                timeframe= TimeFrame.Day,
                                start = datetime.now() - timedelta(days= day_interval)
                        )

    print("\n~~~~~~~~~~~~~~~~~~\nBars\n~~~~~~~~~~~~~~~~")
    data_bars = main.data_client.get_stock_bars(stock_bars_request)
    data_bars_df = data_bars.df
    data_size= len(data_bars[ticker])
    if (data_size < 5): #if data size isn't the day interval cause of weekend, add those missing days
        sleep(1)
        stock_bars_request = StockBarsRequest(
                                symbol_or_symbols = ticker, 
                                timeframe= TimeFrame.Day,
                                start = datetime.now() - timedelta(days= day_interval + (day_interval-data_size))
                        )
        data_bars = main.data_client.get_stock_bars(stock_bars_request)
        data_bars_df = data_bars.df
    print(data_bars_df)
    close_list = []
    for day in data_bars[ticker]:
        val = day.close
        close_list.append(val)
    print(numpy.mean(close_list))

    x1 = [4,3,2,1,0]
    plt.plot(x1, close_list, color= "green", label="Closing Price")
    plt.xlabel('Days Ago')
    plt.ylabel('Moving Average Pirce')
    plt.gca().invert_xaxis()
    plt.show()


    # stock_quotes_request = StockQuotesRequest(
    #         symbol_or_symbols= ['AAPL','GOOGL'], 
    #         start =  datetime.today() - timedelta(days= day_interval),
    #         limit=10
    # )

    # print("~~~~~~~~~~~~~~~~~~\nQuotes\n~~~~~~~~~~~~~~~~")
    # data_quotes = data_client.get_stock_quotes(stock_quotes_request)
    # data_quotes_df = data_quotes.df
    # print(data_quotes_df)