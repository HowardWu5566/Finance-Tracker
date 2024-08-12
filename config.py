import os

class Config:
    DATABASE = os.environ.get('DATABASE', 'datafile.db') 
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    CURRENCY_API_URL = 'https://tw.rter.info/capi.php'
    STOCK_API_URL = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&stockNo='