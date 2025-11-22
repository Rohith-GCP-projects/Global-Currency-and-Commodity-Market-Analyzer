import requests
import os 
import datetime

API_KEY = os.getenv('EXCHANGERATE_API_KEY')

BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# CURRENCY_PAIRS = ["INR", "EUR", "USD", "JPY", "GBP"]
def get_forex_data(base_currency):

    url = f"{BASE_URL}{base_currency}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        return {"error": data.get("error-type")}, 500
    
    timestamp = datetime.datetime.now().isoformat()
    currency_list = sorted(list(data["conversion_rates"].keys()))

    # for currency, rate in di.items():
	#   list.append(currency)

    return {
        "base": data["base_code"], 
        "currency_list": currency_list, 
        "timestamp": timestamp,
        "all_rates": data.get("conversion_rates", {}) # Returning all rates just in case
    }
