from flask import *
import requests
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from datetime import datetime
from yahoo_finance import *

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("home.html")

@app.route('/home')
def homepage():
    return render_template("home.html")

@app.route('/',methods=['POST'])
def my_form_post():
    text = request.form.get('stock')
    if("none" in text):
        my_form_post()
    y = Share(text)
    t = str(datetime.now())
    date = t[:10]
    price = float(y.get_price())
    change = float(y.get_change())
    book = float(y.get_book_value())
    p_b = 1

    if(book != 0):
        p_b = price/book

    short = float(y.get_short_ratio())
    vol = float(y.get_avg_daily_volume())
    capital = (y.get_market_cap())
    result = 0
    show = ""

    if(change == 0 and short == 0):
        result = 0
    elif(short < 2):
        result = 1
    elif(short > 3 and vol >1):
        result = -1
    elif(change < 0 and vol > 1):
        result = -1
    elif(change > 0 and vol < 1):
        if(p_b > 1):
            result = 1
        elif(p_b < 1):
            result = -1

    up = 1

    if(change < 0):
        up = -1
    show = "\nCurrent price of the stock is : " + str(price)

    if(up >= 0):
        show = show + "\nStocks are up by " + str(change)
    else:
        show = show + "\nStocks are down by : " + str(change)
        
    if(capital is not None):
        show = show + "\nMarket Capitalisation of the current stock is " + capital

    if(result == -1):
        show = show + "\n\nAccording to our analysis, the stocks are vulnerable to fall.\nSo it's not advised to invest in them."
    elif(result == 0):
        show = show + "\n\nAccording to our analysis, the stocks seem to be neutral.\nSo, nothing can be said regarding investing in them."
    else:
        show = show + "\n\nAccording to our analysis, the stocks seem to be going up.\nSo, it's the right time to invest in them."

    data1 = web.get_data_yahoo(str(text), start = '2015-01-01', end = date)[['Close']]
    data1.plot(subplots = True, figsize = (30, 12))
    plt.title(text,fontsize=30)
    plt.figtext(0.50, -0.001, show,verticalalignment='bottom', horizontalalignment='center',color='green', fontsize=15)
    plt.legend(loc = 'best')
    plt.savefig("C:/Python34/financial hackathon/static/p1.png")
    return send_from_directory("static","p1.png")

if(__name__ == '__main__'):
    app.run(debug=True,host="192.168.1.100")
