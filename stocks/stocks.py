import requests
import os

API_KEY = os.getenv("STOCK_API_KEY")

def fetch_symbol_data(keyword):
    function = "SYMBOL_SEARCH"
    SERACH_POINT_URL = f"https://www.alphavantage.co/query?function={function}&keywords={keyword}&apikey={API_KEY}"    

    response = requests.get(SERACH_POINT_URL)
    data = response.json()

    matches = data.get("bestMatches", [])

    symbols = []
    for match in matches: 
        symbols.append(match.get("1. symbol"))

    return symbols

def get_stocks_data(symbol):
    function = "TIME_SERIES_DAILY"
    URL = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}"
    
    response = requests.get(URL)
    data = response.json()

    return data