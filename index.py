from flask import Flask

from config import Config
from database import init_app
from path import home, cash_form, cash_delete, stock_form
from error import handle_404, handle_500

app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

app.add_url_rule('/', 'home', home)
app.add_url_rule('/cash', 'cash_form', cash_form, methods=['GET', 'POST'])
app.add_url_rule('/cash-delete', 'cash_delete', cash_delete, methods=['POST'])
app.add_url_rule('/stock', 'stock_form', stock_form, methods=['GET', 'POST'])

app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])