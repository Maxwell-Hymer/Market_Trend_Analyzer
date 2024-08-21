#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File Name: Stock_Code_Lib
================================================================================

A collection of methods for accessing stock symbols and their corresponding data
.. moduleauthor:: Maxwell Hymer <maxhymertime@gmail.com>
.. moduleversion:: 1.0
.. date:: 2024-08-12
'''

import yfinance as yf
import pandas as pd
import re

adl_values = []

def get_stock(stock_url: str):
    '''
    Extract the stock symbol from a Yahoo Finance URL.

    Args:
        stock_url (str): The URL of the stock's Yahoo Finance page,
                         e.g. "https://finance.yahoo.com/quote/COST/history/"

    Returns:
        str: The stock symbol, e.g. "COST"
    '''
    
    ticker = stock_url.split('/')[-3] 
    stock_info = yf.Ticker(ticker)
    return stock_info.info['symbol']


def find_stock_url(stock_name: str):
    '''
    Generate a Yahoo Finance URL from a stock symbol.

    Args:
        stock_name (str): The stock symbol, e.g. "COST"

    Returns:
        str: The URL of the stock's Yahoo Finance page, e.g. "https://finance.yahoo.com/quote/COST/history/"
             or "Invalid Ticker Symbol" if the input is invalid
    '''
    
    url_format = "https://finance.yahoo.com/quote/{}/history/" # constant  <-
    caps_regex = r'^[A-Z]+$' # constant  <-
    
    if re.fullmatch(caps_regex, stock_name):
        # Replaces {} with stock name ex: "https://finance.yahoo.com/quote/{stock_name}/history/"
        return f"{url_format}".format(stock_name) 
    
    return "Invalid Ticker Symbol"


def get_stock_snapshot (stock_name: str):
    '''
    Get a snapshot of the stock's recent performance.

    Args:
        stock_name (str): Stock ticker symbol (e.g. "COST")

    Returns:
        pd.DataFrame: A DataFrame with the latest values for Close, MA21, MA50, and MA10,
                      with a meaningful index value.

    Description:
        This function retrieves the stock's historical data for the past 6 months,
        calculates the moving averages for the past 21, 50, and 10 days, and
        returns a DataFrame with the latest values.
    '''   
    stock = yf.Ticker(stock_name)
    data = stock.history(period="6mo") # set this as a constant  <-
    
    # Calculate the moving averages
    ma21 = data['Close'].rolling(window=21).mean().iloc[-1]
    ma50 = data['Close'].rolling(window=50).mean().iloc[-1]
    ma10 = data['Close'].rolling(window=10).mean().iloc[-1]
    
    snapshot = {'Close': data['Close'].iloc[-1], 'MA21': ma21, 'MA50': ma50, 'MA10': ma10}
    
    return pd.DataFrame([snapshot], index=[data.index[-1]])

def extract_snapshot_values (snapshot: pd.DataFrame):
    '''
    Extract values from a stock snapshot DataFrame.

    Args:
        snapshot (pd.DataFrame): A DataFrame with the stock's snapshot data,
                                  typically obtained from get_stock_snapshot.

    Returns:
        tuple: A tuple containing the Close, MA21, MA50, and MA10 values.
    '''  
    close = snapshot['Close'].iloc[0]
    ma21 = snapshot['MA21'].iloc[0]
    ma50 = snapshot['MA50'].iloc[0]
    ma10 = snapshot['MA10'].iloc[0]
    
    return close, ma21, ma50, ma10

def calculate_stage_2 (stock_name: str, close: float):
    '''
    Determines whether a stock is in a bullish trend (Stage 2) based on its current price and 150-day simple moving average (SMA150).
    
    A stock is considered to be in Stage 2 if its current closing price is above its 150-day SMA, indicating a potential uptrend.
    
    Args:
        stock_name (string): the ticker symbol of the stock to evaluate
        close (float): the current closing price of the stock
        
    Returns:
        boolean: True if the stock is in Stage 2 (i.e., current close is above SMA150), False otherwise
        
    '''
    stock = yf.Ticker(stock_name)
    data = stock.history(period="1y")
    condition = False 
    
    sma150 = data['Close'].rolling(window=150).mean().iloc[-1]
    
    if close > sma150:
        condition = True
    
    return condition
    
def high_liquitity_indicator (stock_name: str):
    '''
    Calculates a simple liquidity indicator for a given stock.
    
    Parameters:
    stock_name (str): The ticker symbol of the stock to analyze.
    
    Returns:
    bool: A boolean indicator indicating whether the stock's current volume is higher than yesterday's volume.
    '''
    indicator = False 
    stock = yf.Ticker(stock_name)
    data = stock.history(period='5d')
    
    current_vol = data['Volume'].iloc[-1]
    yesterday_vol = data['Volume'].iloc[-2]
    
    if current_vol > yesterday_vol:
        indicator = True
    
    return indicator

def get_today_yesterday_adl(ticker):
    """
    Get today's and yesterday's Accumulation/Distribution Line (ADL) values for a given ticker

    Parameters:
    ticker (str): Stock ticker symbol

    Returns:
    today_adl (float): Today's ADL value
    yesterday_adl (float): Yesterday's ADL value
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period='1mo')

    # Calculate the ADL values
    data['ADL'] = 0.0  # Initialize the 'ADL' column with float values
    data.iloc[0, data.columns.get_loc('ADL')] = (((data.iloc[0]['Close'] - data.iloc[0]['Low']) - (data.iloc[0]['High'] - data.iloc[0]['Close'])) / (data.iloc[0]['High'] - data.iloc[0]['Low'])) * data.iloc[0]['Volume']

    for i in range(1, len(data)):
        money_flow_multiplier = ((data.iloc[i]['Close'] - data.iloc[i]['Low']) - (data.iloc[i]['High'] - data.iloc[i]['Close'])) / (data.iloc[i]['High'] - data.iloc[i]['Low'])
        money_flow_volume = money_flow_multiplier * data.iloc[i]['Volume']
        data.iloc[i, data.columns.get_loc('ADL')] = data.iloc[i-1, data.columns.get_loc('ADL')] + money_flow_volume
        
    pd.options.display.float_format = '{:.2f}'.format
    
    print(data)
    
    today_adl = data.iloc[-1, data.columns.get_loc('ADL')]
    yesterday_adl = data.iloc[-2, data.columns.get_loc('ADL')]
    
    return today_adl, yesterday_adl
    

def main():
    print("This is for test purposes only\n===============================================================")
    ticker_symbol = "https://finance.yahoo.com/quote/COST/history/"
    
    stock_symbol = get_stock(ticker_symbol)
    stock_url = find_stock_url(stock_symbol)
    stock_url_b = find_stock_url("teD")
    
    
    print(f"The stock symbol is: {stock_symbol}")
    
    print(f"The stock URL is: {stock_url}")
    print(f"The stock URL is: {stock_url_b}")
    
    snapshot = get_stock_snapshot(stock_symbol)
    
    close, ma21, ma50, ma10 = extract_snapshot_values(snapshot)
    
    print(f"\nClose: {close}")
    print(f"\nMA21: {ma21}")
    print(f"\nMA50: {ma50}")
    print(f"\nMA10: {ma10}\n")

    is_stage_2 = calculate_stage_2(stock_symbol, close)
    
    print(f"stage 2: {is_stage_2}")
    
    high_liquidity = high_liquitity_indicator(stock_symbol)
    
    print(f"\nHigh Liquidity: {high_liquidity}\n")
    
    #hist = pd.read_csv('your_data.csv', index_col='Date', parse_dates=['Date'])

    # Calculate the ADL
    adl = get_today_yesterday_adl(stock_symbol)
    


if __name__ == "__main__":
    main()