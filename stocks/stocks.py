import requests
import os
from google.cloud import bigquery

API_KEY = os.getenv("STOCK_API_KEY")
client = bigquery.Client()


def fetch_symbol_data(keyword):
    function = "SYMBOL_SEARCH"
    SERACH_POINT_URL = f"https://www.alphavantage.co/query?function={function}&keywords={keyword}&apikey={API_KEY}"    

    response = requests.get(SERACH_POINT_URL)
    data = response.json()

    matches = data.get("bestMatches", [])

    symbols = []
    names = []
    for match in matches: 
        symbols.append(match.get("1. symbol"))
        names.append(match.get("2. name"))

    return (symbols, names)

def get_stocks_data(symbol):
    function = "TIME_SERIES_DAILY"
    URL = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}"
    
    response = requests.get(URL)
    data = response.json()
    
    return data.get("Time Series (Daily)", {})

def insert_stock_data(symbol, data):

    rows = []

    for date, values in data.items():
        rows.append({
            "symbol": symbol,
            "date": date,
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        })

    table_id = "commodity-market-analyzer.stocks_dataset.stocks_dataset"
    errors = client.insert_rows_json(table_id, rows)

    if errors:
        print("Insert errors:", errors)