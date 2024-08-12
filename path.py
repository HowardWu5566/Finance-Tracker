from flask import render_template, request, redirect, url_for
from database import execute_query
from utils import get_currency_rate, calculate_stock_info, create_pie_chart
import math
import os

def home():
    cash_result = execute_query("SELECT * FROM cash")

    tw_dollars = sum(float(data[1]) if data[1] and data[1] != '' else 0 for data in cash_result)
    us_dollars = sum(float(data[2]) if data[2] and data[2] != '' else 0 for data in cash_result)

    exchange_rate = get_currency_rate()
    if exchange_rate is None:
        return handle_500('error.html', message="無法獲取匯率")

    total = math.floor(tw_dollars + us_dollars * exchange_rate)


    stock_result = execute_query("SELECT * FROM stock")
    stock_info, total_stock_value = calculate_stock_info(stock_result)


    # pie chart
    if stock_info:
        create_pie_chart([s['stock_id'] for s in stock_info], [s['total_value'] for s in stock_info], "piechart.jpg")
    
    if us_dollars or tw_dollars or total_stock_value:
        create_pie_chart(['USD', 'TWD', 'Stock'], [us_dollars * exchange_rate, tw_dollars, total_stock_value], "piechart2.jpg")


    data = {
        'show_pic1': os.path.exists('static/piechart.jpg'),
        'show_pic2': os.path.exists('static/piechart2.jpg'),
        'total': total,
        'currency': exchange_rate,
        'us_dollars': us_dollars,
        'tw_dollars': tw_dollars,
        'cash_result': cash_result,
        'stock_info': stock_info
    }

    return render_template('index.html', data=data)


def cash_form():
    if request.method == 'POST':
        tw_dollars = 0
        us_dollars = 0
        if request.values['tw-dollars'] != '':
            tw_dollars = request.values['tw-dollars']
        if request.values['us-dollars'] != '':
            us_dollars = request.values['us-dollars']
        note = request.form.get('note', '')
        date = request.form.get('date')

        try:
            tw_dollars = int(tw_dollars)
            us_dollars = float(us_dollars)
        except ValueError:
            return handle_500('error.html', message="資料格式錯誤")

        execute_query(
            "INSERT INTO cash (taiwanese_dollars, us_dollars, note, date_info) VALUES (?, ?, ?, ?)",
            (tw_dollars, us_dollars, note, date)
        )
        return redirect(url_for('home'))
    
    return render_template('cash.html')


def cash_delete():
    transaction_id = request.form.get('id')
    execute_query("DELETE FROM cash WHERE transaction_id = ?", (transaction_id,))
    return redirect(url_for('home'))


def stock_form():
    if request.method == 'POST':
        stock_id = request.form.get('stock-id')
        stock_num = request.form.get('stock-num')
        stock_price = request.form.get('stock-price')
        processing_fee = request.form.get('processing-fee', 0)
        tax = request.form.get('tax', 0)
        date = request.form.get('date')

        execute_query(
            "INSERT INTO stock (stock_id, stock_num, stock_price, processing_fee, tax, date_info) VALUES (?, ?, ?, ?, ?, ?)",
            (stock_id, stock_num, stock_price, processing_fee, tax, date)
        )
        return redirect(url_for('home'))
    
    return render_template('stock.html')