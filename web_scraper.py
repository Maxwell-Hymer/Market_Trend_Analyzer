import requests as req
import yfinance as yf
from bs4 import BeautifulSoup as beasoup

# This program is to test how web scraping works with python may possibly become a separate code to be imported
def main():
    url = "https://finance.yahoo.com/quote/COST/"
    
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
        
    
    
if __name__ == "__main__":
    main()