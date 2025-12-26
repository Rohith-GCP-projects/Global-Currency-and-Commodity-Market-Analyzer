import requests
import os
from google.cloud import bigquery

API_KEY = os.getenv("STOCK_API_KEY")
client = bigquery.Client(project="commodity-market-analyzer")


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

def get_max_date(symbol):
    table_id = "commodity-market-analyzer.stocks_dataset.stocks_dataset"
    query = f"""
        SELECT MAX(date) as max_date
        FROM `{table_id}`
        WHERE symbol = @symbol
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("symbol", "STRING", symbol),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    results = query_job.result()
    
    for row in results:
        return row.max_date
    return None

def insert_stock_data(symbol, data):
    max_date = get_max_date(symbol)
    print(f"Max date for {symbol} in BigQuery: {max_date}")

    rows = []

    for date, values in data.items():
        # Only add rows that are newer than the max_date in BigQuery
        if max_date is None or date > str(max_date):
            rows.append({
                "symbol": symbol,
                "date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            })

    if not rows:
        print(f"No new data to insert for {symbol}.")
        return

    print(f"Inserting {len(rows)} new rows for {symbol}.")
    table_id = "commodity-market-analyzer.stocks_dataset.stocks_dataset"
    errors = client.insert_rows_json(table_id, rows)

    if errors:
        print("Insert errors:", errors)

    query = '''
        CREATE OR REPLACE TABLE `commodity-market-analyzer.stocks_dataset.stock_dataset_view`
        AS SELECT * FROM `commodity-market-analyzer.stocks_dataset.stocks_dataset` WHERE symbol = @symbol
    '''
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("symbol", "STRING", symbol),
        ]
    )
    query_job = client.query(query, job_config=job_config, location="asia-south1")
    results = query_job.result()