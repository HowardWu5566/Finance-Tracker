import requests
import math
import matplotlib
import matplotlib.pyplot as plt
from config import Config
matplotlib.use('agg')

def get_currency_rate():
    try:
        r = requests.get(Config.CURRENCY_API_URL)
        r.raise_for_status()
        currency = r.json()
        return currency['USDTWD']['Exrate']
    except requests.RequestException as e:
        print(f"Error fetching currency rate: {e}")
        return None

def get_stock_price(stock_id):
    try:
        url = f"{Config.STOCK_API_URL}{stock_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price_array = data['data']
        return float(price_array[-1][6])
    except requests.RequestException as e:
        print(f"Error fetching stock price: {e}")
        return None

def calculate_stock_info(stock_data):
    stock_info = []
    total_stock_value = 0
    for stock in set(data[1] for data in stock_data):
        stock_records = [d for d in stock_data if d[1] == stock]
        shares = sum(d[2] for d in stock_records)
        stock_cost = sum(d[2] * d[3] + d[4] + d[5] for d in stock_records)
        current_price = get_stock_price(stock)
        if current_price is None:
            continue
        total_value = round(current_price * shares)
        total_stock_value += total_value
        average_cost = round(stock_cost / shares, 2)
        rate_of_return = round((total_value - stock_cost) * 100 / stock_cost, 2)
        stock_info.append({
            'stock_id': stock,
            'stock_cost': stock_cost,
            'total_value': total_value,
            'average_cost': average_cost,
            'shares': shares,
            'current_price': current_price,
            'rate_of_return': rate_of_return
        })
    
    for stock in stock_info:
        stock['value_percentage'] = round(stock['total_value'] * 100 / total_stock_value, 2) if total_stock_value else 0

    return stock_info, total_stock_value

def create_pie_chart(labels, sizes, filename):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(sizes, labels=labels, autopct=None, shadow=None)
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.savefig(f"static/{filename}", dpi=200)
    plt.close(fig)