# admin/product_sidebar.py
import sqlite3
from flask import Blueprint, render_template, request, redirect

product_bp = Blueprint('product', __name__, url_prefix='/admin')
BASE_URL = 'http://127.0.0.1:5050'


# @product_bp.route('/product')
# def product():
#     return render_template('admin/product/product.html')


@product_bp.route('/product')
def product_list():
    conn = sqlite3.connect('midterm.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM products')
    rows = cur.fetchall()
    return render_template('admin/product/product.html', BASE_URL=BASE_URL, rows=rows)


@product_bp.route('/edit_product/<int:ID>', methods=['GET', 'POST'])
def edit_product(ID):
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']
        image = request.form['image']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("UPDATE products SET category_id=?, name=?, cost=?, price=?, image=?, status=? WHERE id=?",
                    (category, name, cost, price, image, status, ID))
        conn.commit()
        conn.close()

        return redirect("/admin/product")  # Redirect to the list page after updating

    else:
        # Display the form with existing data
        conn = sqlite3.connect('midterm.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM products WHERE ID={ID}')
        rows = cur.fetchall()
        conn.close()

        return render_template('admin/product/editproduct.html', rows=rows)


@product_bp.route('/delete_row/<ID>', methods=['GET', 'POST'])
def delete_student(ID):
    conn = sqlite3.connect('midterm.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM products WHERE id={ID}")
    cur.execute(f"DELETE FROM sqlite_sequence WHERE name='products'")
    cur.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('products', 1)")
    conn.commit()
    conn.close()

    return redirect("/admin/product")


@product_bp.route('/product/add_product', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']
        image = request.form['image']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO products (category_id, name, cost, price, image, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (category, name, cost, price, image, status))
        conn.commit()
        conn.close()

        return redirect("/admin/product")

    else:
        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute('SELECT name FROM categorys')
        categories = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('admin/product/addproduct.html', categories=categories)