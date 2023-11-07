# admin/product_sidebar.py
import sqlite3
from flask import Blueprint, render_template, request, redirect, flash

user_bp = Blueprint('user', __name__, url_prefix='/admin')
BASE_URL = 'http://127.0.0.1:5050'


# @product_bp.route('/product')
# def product():
#     return render_template('admin/product/product.html')


@user_bp.route('/user')
def user_list():
    conn = sqlite3.connect('midterm.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    return render_template('admin/user/user.html', BASE_URL=BASE_URL, rows=rows)


@user_bp.route('/user/edit_user/<int:ID>', methods=['GET', 'POST'])
def edit_user(ID):
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("UPDATE users SET name=?, image=?, status=? WHERE id=?",
                    (name, image, status, ID))
        conn.commit()
        conn.close()

        flash('Form submitted successfully!', 'success')
        return redirect("/admin/user")  # Redirect to the list page after updating

    else:
        # Display the form with existing data
        conn = sqlite3.connect('midterm.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM users WHERE ID={ID}')
        rows = cur.fetchall()
        conn.close()

        return render_template('admin/user/edituser.html', rows=rows)


@user_bp.route('/user/delete_user/<ID>', methods=['GET', 'POST'])
def delete_user(ID):
    conn = sqlite3.connect('midterm.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users WHERE id={ID}")
    cur.execute(f"DELETE FROM sqlite_sequence WHERE name='users'")
    cur.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('users', 1)")
    conn.commit()
    conn.close()

    flash('Form deleted successfully!', 'success')
    return redirect("/admin/user")


@user_bp.route('/user/add_customer', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, image, status) VALUES (?, ?, ?)",
                    (name, image, status))
        conn.commit()
        conn.close()

        flash('Form submitted successfully!', 'success')
        return redirect("/admin/user")

    else:
        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute('SELECT name FROM users')
        users = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('admin/user/adduser.html', users=users)