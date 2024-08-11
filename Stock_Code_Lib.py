# ============================================================================
# File Name: Stock_Code_Lib
# ============================================================================
# Author: Maxwell Hymer
# Date: 8/9/2024
# ============================================================================
# Description: This code will contain a series of methods and functions that
# will be used in other parts of the code just various methods to avoid
# clutter
# ============================================================================
import yfinance as yf

def get_stock(stock_url: str):
    '''
    Function that will take the URL link and return the name of the stock
    =====================================================================
    Args: stock_url (string): "https://finance.yahoo.com/quote/COST/history/"
        
    Splits the url string into a list of substrings using / as a delimiter and sets ticker to the third to last element in the list
    
    Creates a ticker obj via yfinance passing the ticker var as the arg which gets the corresponding finanical data for the stock
    
    Returns: the name of the stock symbol from the stock_info var
    '''
    
    ticker = stock_url.split('/')[-3] 
    stock_info = yf.Ticker(ticker)
    return stock_info.info['symbol']

def main():
    stock_symbol = get_stock("https://finance.yahoo.com/quote/COST/history/")
    print(f"The stock symbol is: {stock_symbol}")

if __name__ == "__main__":
    main()