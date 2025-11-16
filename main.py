import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGERATE_API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

# Add currencies you want to track
CURRENCY_PAIRS = [
    "INR",
    "EUR",
    "USD",
    "JPY", 
    "GBP"
]

def fetch_forex_rates():
    try:
        response = requests.get(BASE_URL)
        data = response.json()

        if data.get("result") != "success":
            raise Exception(f"API Error: {data.get('error-type')}")

        rates = data["conversion_rates"]

        forex_data = []
        # timestamp = data["time_last_update_utc"]
        timestamp = datetime.utcnow().isoformat()

        for currency in CURRENCY_PAIRS:
            forex_data.append({
                "base": "USD",
                "currency": currency,
                "rate": rates.get(currency),
                "timestamp": timestamp
            })

        return forex_data

    except Exception as e:
        print("Error fetching forex rates:", e)
        return None


if __name__ == "__main__":
    result = fetch_forex_rates()
    print(result)
