# admin/category.py
import sqlite3

from flask import Blueprint, render_template, request, redirect

currency_bp = Blueprint('currency', __name__, url_prefix='/admin')
BASE_URL = 'http://127.0.0.1:5050'


# @product_bp.route('/product')
# def product():
#     return render_template('admin/product/product.html')


@currency_bp.route('/currency')
def currency_list():
    conn = sqlite3.connect('midterm.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM currencys')
    rows = cur.fetchall()
    return render_template('admin/currency/currency.html', BASE_URL=BASE_URL, rows=rows)


@currency_bp.route('/currency/edit_currency/<int:ID>', methods=['GET', 'POST'])
def edit_currency(ID):
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        symbol = request.form['code']
        is_default = request.form['default']
        selloutprice = request.form['selloutprice']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("UPDATE currencys SET name=?, code=?, symbol=?, is_default=?, sell_out_price=? WHERE id=?",
                    (name, code, symbol, is_default, selloutprice, ID))
        conn.commit()
        conn.close()

        return redirect("/admin/currency")  # Redirect to the list page after updating

    else:
        # Display the form with existing data
        conn = sqlite3.connect('midterm.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM currencys WHERE ID={ID}')
        rows = cur.fetchall()
        conn.close()

        return render_template('admin/currency/editcurrency.html', rows=rows)


@currency_bp.route('/currency/delete_row/<ID>', methods=['GET', 'POST'])
def delete_category(ID):
    conn = sqlite3.connect('midterm.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM currencys WHERE id={ID}")
    cur.execute(f"DELETE FROM sqlite_sequence WHERE name='currencys'")
    cur.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('currencys', 1)")
    conn.commit()
    conn.close()

    return redirect("/admin/currency")


@currency_bp.route('/currency/add_currency', methods=['GET','POST'])
def add_currency():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        symbol = request.form['code']
        is_default = request.form['default']
        selloutprice = request.form['selloutprice']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO currencys (name, code, symbol, is_default, sell_out_price) VALUES (?, ?, ?, ?, ?)",
                    (name, code, symbol, is_default, selloutprice))
        conn.commit()
        conn.close()

        return redirect("/admin/currency")

    else:
        return render_template('admin/currency/addcurrency.html')