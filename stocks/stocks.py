import requests
import os

API_KEY = os.getenv("STOCK_API_KEY")
func = "TIME_SERIES_DAILY"
kwd = "TSLA"

URL = f"https://www.alphavantage.co/query?function={func}&symbol={kwd}&apikey={API_KEY}"

def get_stocks_data(keyword):
    function = "SYMBOL_SEARCH"
    SERACH_POINT_URL = f"https://www.alphavantage.co/query?function={function}&keywords={keyword}&apikey={API_KEY}"    

    response = requests.get(SERACH_POINT_URL)
    data = response.json()

    matches = data.get("bestMatches", [])

    symbols = []
    for match in matches: 
        symbols.append(match.get("1. symbol"))

    return {
        "data": symbols
    }