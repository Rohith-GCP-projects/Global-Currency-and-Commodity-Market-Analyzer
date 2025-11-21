from flask import Flask, render_template
from forex.forex import get_forex_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/forex')
def forex():
    data = get_forex_data()
    return render_template('forex.html', data=data)