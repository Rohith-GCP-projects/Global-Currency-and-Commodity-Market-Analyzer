from flask import Flask, render_template, request  # Import request
from forex.forex import get_forex_data
from stocks.stocks import get_stocks_data, fetch_symbol_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/forex', methods=['GET', 'POST'])
def forex_page():
    # Default values
    base_currency = 'USD'
    target_currency = 'EUR'
    amount = 1
    result = None
    rate = None

    # If the user submitted the form (clicked Convert)
    if request.method == 'POST':
        base_currency = request.form.get('base_currency')
        target_currency = request.form.get('target_currency')
        amount = float(request.form.get('amount'))

    # Get data from your forex.py function
    data = get_forex_data(base_currency)

    # Calculate the result if we have rates
    if request.method == 'POST' and 'all_rates' in data:
        rates = data['all_rates']
        if target_currency in rates:
            rate = rates[target_currency]
            result = round(amount * rate, 2)

    return render_template('forex.html', 
                           data=data, 
                           result=result,
                           rate=rate,
                           selected_base=base_currency,
                           selected_target=target_currency,
                           selected_amount=amount)

@app.route('/stocks', methods=['GET', 'POST'])
def stocks_page():
    stocks_data = None 
    keyword = None

    if request.method == 'POST':
        keyword = request.form.get('SEARCH_KEYWORD')
        if keyword:
            symbol_list, symbol_name_list = fetch_symbol_data(keyword)
            return render_template('stocks.html', symbol_list=symbol_list, symbol_name_list=symbol_name_list)

    symbol = request.args.get('SEARCH_KEYWORD')
    if symbol:
        stock_details = get_stocks_data(symbol)
        insert_stock_data(symbol, stock_details)
        return render_template('stocks.html', stock_details=stock_details)
    
    return render_template('stocks.html')

if __name__ == '__main__':
    app.run(debug=True)