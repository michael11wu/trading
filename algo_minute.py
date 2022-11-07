"""
Per X Minute Trading Algorithm.

Can use on one or multiple tickers
"""

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta

from trading_client import orderStock, sellStock
from API_keys import API_KEY, SECRET_KEY

import numpy
import matplotlib.pyplot as plt
from time import sleep

data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

close_history = [] 
plot_minute_moving_average = []
plot_minute_closing = []

def moving_minute_average(moving_average: int, ticker: str, pos_held: bool, interval: int):
    """
    Gathers [moving_average] moving average of a ticker and buys a share if the closing price of that interval crosses above the moving average and sells if closing price crosses below moving average

    Args:
        moving_average (int): Span of each moving average
        ticker (str): Symbol of Stock to be watched
        pos_held (bool): value for if the position is already held
        interval (int): How long to wait for getting moving average. Keep at (1) for every minute. It will run every x minutes and the moving average will span x * moving_average minutes
    """


    #Setting up bar requests
    stock_bars_request = StockBarsRequest(
                                symbol_or_symbols= ticker, 
                                timeframe= TimeFrame(interval, TimeFrameUnit.Minute),
                                start = datetime.now() - timedelta(minutes= moving_average) * interval,
                                end = datetime.now()
                        )

    data_bars = data_client.get_stock_bars(stock_bars_request)
    data_bars_df = data_bars.df
    print(data_bars_df)

    for day in data_bars[ticker]:
        val = day.close
        close_history.append(val)

    current_moving_average = numpy.mean(close_history)

    print(str(moving_average * interval) + " minute moving average: " + str(current_moving_average))
    print("Closing price of Current Minute: " + str(close_history[-1]))

    #Need at least two minutes of data
    if (len(plot_minute_closing) > 0):
        #If closing price crosses above moving average and position isn't already held, buy a share
        if ((current_moving_average < close_history[-1] - 0.01) and (plot_minute_moving_average[-1] > plot_minute_closing[-1]) and not pos_held):
            print("Buying share")
            orderStock(ticker,1)
            pos_held = True
        
        #If closing price cross below moving average and position is held, sell the share
        elif ((current_moving_average > close_history[-1] + 0.01) and (plot_minute_moving_average[-1] < plot_minute_closing[-1]) and pos_held):
            print("Selling share")
            sellStock(ticker,1)
            pos_held = False
        else:
            print("No selling or buying")

    #Building the plot points
    plot_minute_closing.append(close_history[-1])
    plot_minute_moving_average.append(current_moving_average)
    return pos_held

def run_ticker(time_to_run: int, ticker: str, moving_average: int, interval: int):
    """
    Runs the moving minute average for x minutes on the ticker specified

    Args:
        time_to_run (int): Value for how many minutes to run for
        ticker (str): Symbol of Stock to watch
        moving_average (int): How long each moving average should span
        interval (int): How long to wait for getting moving average. Keep at (1) for every minute. It will run every x minutes and the moving average will span x * moving_average minutes
    """

    x1 = []
    pos_held = False
    while (time_to_run > 0):
        pos_held = moving_minute_average(moving_average,ticker,pos_held)
        #Keep program running until positions are sold
        if (pos_held and time_to_run == 1):
            print("Keep running until positions are sold")
        else:
            time_to_run -= 1
        x1.append(time_to_run)
        sleep(60)
    
    plt.plot(x1, plot_minute_closing, marker='o', color= "green", label="Closing Price")
    plt.plot(x1, plot_minute_moving_average,marker='x', color= "Red", label="Moving Average Price")
    plt.title(label=ticker)
    plt.xlabel('Minutes Ago')
    plt.ylabel('Price')
    plt.gca().invert_xaxis()
    plt.legend(loc="best")
    plt.show()



plot_minute_closing_multiple = []
plot_minute_moving_average_multiple = []
#Run with multiple tickers
def multiple_moving_averages(moving_average: int, tickers: list[str], pos_held: bool, interval: int):
    """
    Gathers [moving_average] moving average of multiple tickers and buys a share if the closing price of that interval crosses above the moving average and sells if closing price crosses below moving average

    Args:
        moving_average (int): Span of moving minute average
        tickers: (List[str]): List of symbols of stocks to be watched
        pos_held (bool): True/False for if the position is already held
        interval (int): How long to wait for getting moving average. Keep at (1) for every minute. It will run every x minutes and the moving average will span x * moving_average minutes
    """

    #Setting up bar requests
    stock_bars_request = StockBarsRequest(
                                symbol_or_symbols= tickers, 
                                timeframe= TimeFrame(interval,TimeFrameUnit.Minute),
                                start = datetime.now() - timedelta(minutes= moving_average)* interval,
                                end = datetime.now()
                        )

    data_bars = data_client.get_stock_bars(stock_bars_request)
    data_bars_df = data_bars.df
    print(data_bars_df)
    for i in range(0,len(tickers)):
        ticker = tickers[i]
        closing_history_multiple = []
        for day in data_bars[ticker]:
            val = day.close
            closing_history_multiple.append(val)

        current_moving_average = numpy.mean(closing_history_multiple)

        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(ticker + " held: " + str(pos_held[i]))
        print(str(moving_average * interval) + " minute moving average: " + str(current_moving_average))
        print("Closing price of Current Minute Span: " + str(closing_history_multiple[-1]))

        #Need at least two minutes of data
        if (len(plot_minute_closing_multiple[i]) > 0):
            #If closing price crosses above moving average and position isn't already held, buy a share
            if ((current_moving_average < closing_history_multiple[-1] - 0.01) and (plot_minute_moving_average_multiple[i][-1] > plot_minute_closing_multiple[i][-1]) and not pos_held[i]):
                print("Buying share")
                orderStock(tickers[i],1)
                pos_held[i] = True
            
            #If closing price cross below moving average and position is held, sell the share
            elif ((current_moving_average > closing_history_multiple[-1] + 0.01) and (plot_minute_moving_average_multiple[i][-1] < plot_minute_closing_multiple[i][-1]) and pos_held[i]):
                print("Selling share")
                sellStock(tickers[i],1)
                pos_held[i] = False
            else:
                print("No selling or buying")

        #Building the plot points
        plot_minute_closing_multiple[i].append(closing_history_multiple[-1])
        plot_minute_moving_average_multiple[i].append(current_moving_average)
    return pos_held

def run_multiple_tickers(time_to_run: int, tickers: list[str], moving_average: int, interval: int):
    """
    Runs the moving minute average for x minutes on the ticker specified

    Args:
        time_to_run (int): Value for how many minutes to run for
        tickers (List[str]): List of symbols of stocks to watch
        moving_average (int): How long each moving average should span
        interval (int): How long to wait for getting moving average. Keep at (1) for every minute. It will run every x minutes and the moving average will span x * moving_average minutes
    """

    x1 = []
    any_pos_held = False
    pos_held = []
    for i in range(0,len(tickers)):
        pos_held.append(False)
        plot_minute_closing_multiple.append([])
        plot_minute_moving_average_multiple.append([])

    while (time_to_run > 0):
        pos_held = multiple_moving_averages(moving_average,tickers,pos_held,interval)
        
        for i in range(0,len(pos_held)):
            print("")

        #Keep program running until positions are sold
        if (any_pos_held and time_to_run == 1):
            print("Keep running until positions are sold") #may cause problems with multiple tickers
        else:
            time_to_run -= 1
        x1.append(time_to_run)

        #wait a minute before running again
        sleep(60)
    
    for i in range(0,len(tickers)):
        plt.plot(x1, plot_minute_closing_multiple[i], marker='o', color= "green", label="Closing Price")
        plt.plot(x1, plot_minute_moving_average_multiple[i],marker='x', color= "Red", label="Moving Average Price")
        plt.title(label=tickers[i])
        plt.xlabel('Minutes Ago')
        plt.ylabel('Price')
        plt.gca().invert_xaxis()
        plt.legend(loc="best")
        plt.show()














