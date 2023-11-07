import randomname
from flask import Flask, render_template, request, redirect
import random
import sqlite3
from route.product import product_bp
from route.category import category_bp
from route.currency import currency_bp
from route.customer import customer_bp
from route.user import user_bp
app = Flask(__name__)
import os
app.secret_key = os.urandom(24)


# conn = sqlite3.connect('midterm.db')
# print('Successfully Connected to databases')
#
#
# conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT,category_id INT NOT NULL,name VARCHAR(255) NOT NULL,cost DECIMAL(10,2) NOT NULL,price DECIMAL(10,2) NOT NULL,image VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL);')
# conn.execute('CREATE TABLE currencys (id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(255) NOT NULL,code VARCHAR(255) NOT NULL,symbol VARCHAR(255) NOT NULL,is_default VARCHAR(255) NOT NULL,sell_out_price DECIMAL(10,2) NOT NULL);')
# conn.execute('CREATE TABLE categorys (id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL);')
# conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(255) NOT NULL,image VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL);')
# conn.execute('CREATE TABLE customers (id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(255) NOT NULL,image VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL);')
# conn.close()


BASE_URL = 'http://127.0.0.1:5050'
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(currency_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(user_bp)


conn = sqlite3.connect('midterm.db')
cur = conn.cursor()
cur.execute('SELECT name FROM categorys')
categories = [row[0] for row in cur.fetchall()]
conn.close()


@app.route('/')
def hello_world():  # put application's code here
    products = []
    for items in range(12):
        products.append({
            'id': 1,
            'pName': randomname.get_name(noun=('shopping')),
            'oPrice': random.randint(10, 200),
            'discount': random.randint(1, 50),
        })
    return render_template('index.html', products=products)


@app.route('/admin')
def admin():
    return redirect("/admin/product")


# @app.route('/admin/product')
# def product_list():
#     conn = sqlite3.connect('midterm.db')
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM products')
#     rows = cur.fetchall()
#     return render_template('admin/product/product.html', BASE_URL=BASE_URL, rows=rows)


if __name__ == '__main__':
    app.run()

