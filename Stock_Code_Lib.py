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
    print(f"\nMA10: {ma10}")

if __name__ == "__main__":
    main()