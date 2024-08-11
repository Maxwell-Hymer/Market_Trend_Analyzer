import requests as req
import yfinance as yf
from bs4 import BeautifulSoup as beasoup

# This program is to test how web scraping works with python may possibly become a separate code to be imported
def main():
    url = "https://finance.yahoo.com/quote/COST/"
    stock = yf.Ticker("COST")
    data = stock.history(period="6mo")
    
    response = req.get(url)
    
    if response.status_code == 200:
        print(f"Scraping: {url}\n")
    
        #Parse the HTML content
        soup = beasoup(response.text, 'html.parser')
        
        # Example: Extract the stock price
        price_tag = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        
        if price_tag:
            price = price_tag.text
            print(f"Current Stock Price: {price}")
        else:
            print("\nPrice tag not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
    print()    
        
    #====================================================================    
        
    # Calculate the moving averages
    data['MA21'] = data['Close'].rolling(window=21).mean()  # 21-day MA
    data['MA50'] = data['Close'].rolling(window=50).mean()  # 50-day MA
    data['MA10'] = data['Close'].rolling(window=10).mean()  # 10-day MA

    # View the last few rows to see the calculated moving averages
    print(data[['Close', 'MA21', 'MA50', 'MA10']].tail())
        
    #====================================================================  
    
if __name__ == "__main__":
    main()