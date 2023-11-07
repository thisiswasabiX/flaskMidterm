# admin/category.py
import sqlite3

from flask import Blueprint, render_template, request, redirect

category_bp = Blueprint('category', __name__, url_prefix='/admin')
BASE_URL = 'http://127.0.0.1:5050'


# @product_bp.route('/product')
# def product():
#     return render_template('admin/product/product.html')


@category_bp.route('/category')
def category_list():
    conn = sqlite3.connect('midterm.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM categorys')
    rows = cur.fetchall()
    return render_template('admin/category/category.html', BASE_URL=BASE_URL, rows=rows)


@category_bp.route('/category/edit_category/<int:ID>', methods=['GET', 'POST'])
def edit_category(ID):
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("UPDATE categorys SET name=?, status=? WHERE id=?",
                    (name, status, ID))
        conn.commit()
        conn.close()

        return redirect("/admin/category")  # Redirect to the list page after updating

    else:
        # Display the form with existing data
        conn = sqlite3.connect('midterm.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM categorys WHERE ID={ID}')
        rows = cur.fetchall()
        conn.close()

        return render_template('admin/category/editcategory.html', rows=rows)


@category_bp.route('/category/delete_row/<ID>', methods=['GET', 'POST'])
def delete_category(ID):
    conn = sqlite3.connect('midterm.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM categorys WHERE id={ID}")
    cur.execute(f"DELETE FROM sqlite_sequence WHERE name='categorys'")
    cur.execute(f"INSERT INTO sqlite_sequence (name, seq) VALUES ('categorys', 1)")
    conn.commit()
    conn.close()

    return redirect("/admin/category")


@category_bp.route('/category/add_category', methods=['GET','POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']

        conn = sqlite3.connect('midterm.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO categorys (name, status) VALUES (?, ?)",
                    (name, status))
        conn.commit()
        conn.close()

        return redirect("/admin/category")

    else:
        return render_template('admin/category/addcategory.html')