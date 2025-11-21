# BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD
# CURRENCY_PAIRS = ["INR", "EUR", "USD", "JPY", "GBP"]



# def fetch_forex_rates(request):
#     try:
#         response = requests.get(BASE_URL)
#         data = response.json()

#         if data.get("result") != "success":
#             return jsonify({"error": data.get("error-type")}), 500

#         rates = data["conversion_rates"]
#         timestamp = datetime.utcnow().isoformat()

#         forex_data = []

#         for currency in CURRENCY_PAIRS:
#             forex_data.append({
#                 "base": "USD",
#                 "currency": currency,
#                 "rate": rates.get(currency),
#                 "timestamp": timestamp
#             })

#         return jsonify(forex_data)