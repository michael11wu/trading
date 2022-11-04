"""
Deals with all trading client actions from ordering/selling stocks to getting position and account information
"""

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType

from API_keys import API_KEY, SECRET_KEY


trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True) 

def orderStock(ticker,quantity):

    """
    Orders a stock of a certain ticker symbol and quantity

    Args:
        ticker: (str) Ticker Symbol of Share
        quantity: (int) quantity of share
    """

    # Setting parameters for our market buy order
    market_order_data = MarketOrderRequest(
                        symbol=ticker,
                        qty=quantity,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                    )

    # Submitting the order and then printing the returned object
    market_order = trading_client.submit_order(market_order_data)
    #for property_name, value in market_order:
    #  print(f"\"{property_name}\": {value}")

def sellStock(ticker,quantity):
    """
    Sells a stock of a certain ticker symbol and quantity

    Args:
        ticker: (str) Ticker Symbol of Share
        quantity: (int) quantity of share
    """

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Sell Info")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Setting parameters for our market buy order
    market_sell_data = MarketOrderRequest(
                        symbol=ticker,
                        qty=quantity,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.DAY
                    )

    # Submitting the order and then printing the returned object
    market_order = trading_client.submit_order(market_sell_data)
    #for property_name, value in market_order:
    #  print(f"\"{property_name}\": {value}")


def printAccountInfo():
    """
    Gets Account Info and Prints it 
    """

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Account info")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    account = trading_client.get_account()
    for property_name, value in account:
        print(f"\"{property_name}\": {value}")

def getPositions():
    """
    Get all positions that account is currently holding
    """
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Positions")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #Get all open positions and print each of them
    positions = trading_client.get_all_positions()
    for position in positions:
        for property_name, value in position:
            print(f"\"{property_name}\": {value}")