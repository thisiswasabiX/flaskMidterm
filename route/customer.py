# admin/product_sidebar.py
import sqlite3
from flask import Blueprint, render_template, request, redirect, flash

customer_bp = Blueprint('customer', __name__, url_prefix='/admin')
BASE_URL = 'http://127.0.0.1:5050'


# @product_bp.route('/product')
# def product():
#     return render_template('admin/product/product.html')


@customer_bp.route('/customer')
def customer_list():
    conn = sqlite3.connect('midterm.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM customers')
    rows = cur.fetchall()
    return render_template('admin/customer/customer.html', BASE_URL=BASE_URL, rows=rows)


@customer_bp.route('/customer/edit_customer/<int:ID>', methods=['GET', 'POST'])
def edit_customer(ID):
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("UPDATE customers SET name=?, image=?, status=? WHERE id=?",
                    (name, image, status, ID))
        conn.commit()
        conn.close()

        return redirect("/admin/customer")  # Redirect to the list page after updating

    else:
        # Display the form with existing data
        conn = sqlite3.connect('midterm.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM customers WHERE ID={ID}')
        rows = cur.fetchall()
        conn.close()

        return render_template('admin/customer/editcustomer.html', rows=rows)


@customer_bp.route('/customer/delete_row/<ID>', methods=['GET', 'POST'])
def delete_customer(ID):
    conn = sqlite3.connect('midterm.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM customers WHERE id={ID}")
    cur.execute(f"DELETE FROM sqlite_sequence WHERE name='customers'")
    cur.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('customers', 1)")
    conn.commit()
    conn.close()

    return redirect("/admin/customer")


@customer_bp.route('/customer/add_customer', methods=['GET','POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO customers (name, image, status) VALUES (?, ?, ?)",
                    (name, image, status))
        conn.commit()
        conn.close()

        flash('Customer added successfully!', 'success')
        return redirect("/admin/customer")

    else:
        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute('SELECT name FROM customers')
        customer = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('admin/customer/addcustomer.html', customers=customer)