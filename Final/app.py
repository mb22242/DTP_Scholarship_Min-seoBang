from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os
import sqlite3

# For Login System
load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
SECRET_KEY = os.getenv("SECRET_KEY")

# For Database
UPLOAD_FOLDER = 'Final/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)
app.secret_key = SECRET_KEY


# Flask Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


class AdminUser(UserMixin):
    # There will only be 1 user, which will be the Admin. 
    id = 1
    username = ADMIN_USERNAME


@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return AdminUser()
    return None

# No longer needed since the database has been created. 
# def init_db():
#     conn = get_db_connection()
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS items (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             item_name TEXT,
#             name TEXT,
#             description TEXT,
#             image_filename TEXT,
#             category TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            login_user(AdminUser())
            return redirect(url_for('admin'))
    return render_template('index.html')


@app.route("/claim")
def claim():
    search_item = request.args.get("item", "").replace(" ", "").lower()
    category = request.args.get("category", "")

    if category:  
        items = items_search(category=category)
    else:        
        items = items_search(item=search_item)

    return render_template("claim.html", items=items)


@app.route('/claim_item/<int:item_id>', methods=['GET', 'POST'])
def claim_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()

    if not item:
        flash("Item not found.")
        return redirect(url_for('claim'))

    return render_template('claim_form.html', item=item)


@app.route('/report', methods = ['GET', 'POST'])
def report():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('report.html')


@app.route('/search', methods=['GET', 'POST'])
def search_public():
    item = request.args.get('item', '')
    items = items_search(item)
    return render_template('claim.html', items=items)


def items_search(item="", category=None):
    conn = get_db_connection()
    raw_item = item.strip().lower() if item else ""
    raw_category = category.strip().lower() if category else ""

    sql = "SELECT * FROM items WHERE 1=1"
    params = []

    # Search by item name
    if raw_item and raw_item != "search:":
        sql += " AND REPLACE(LOWER(item_name), ' ', '') LIKE ?"
        params.append(f"%{raw_item}%")

    # Filter by category
    if raw_category and raw_category != "all":
        sql += " AND TRIM(LOWER(category)) = ?"
        params.append(raw_category)

    items = conn.execute(sql, params).fetchall()
    conn.close()

    if not items:
        flash(f"No items were found for '{category}'." if category else "No items found.")
    return items


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    item = request.args.get("item", "").replace(" ", "").lower()
    category = request.args.get("category", "All")

    # Pass both parameters so items_search() can combine filters properly
    items = items_search(item=item, category=category)

    return render_template("admin.html", username=current_user.username, items=items)

   
@app.route('/admin/search', methods=['GET', 'POST'])
@login_required
def search_admin():
    item = request.args.get('item', '')
    items = items_search(item)
    return render_template('admin.html', username=current_user.username, items=items)


@app.route('/admin/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        item_name = request.form['item_name']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        image = request.files['image']
        
    
        # Save image
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # Save data to database
        conn = get_db_connection()
        conn.execute('INSERT INTO items (item_name, name, description, image_filename, category) VALUES (?, ?, ?, ?, ?)', (item_name, name, description, image.filename, category))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))
    return render_template('upload.html')


@app.route('/admin/update/<int:id>', methods=['POST', 'GET'])
def update_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    conn.close()

    categories = [
        "Clothing and Accessories",
        "Electronics",
        "Stationery",
        "Personal Items",
        "Jewellery",
        "Sports Equipment",
        "Miscellaneous"
    ]

    if request.method == 'POST':
        item_name = request.form['item_name']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']

        conn = get_db_connection()
        conn.execute('''
            UPDATE items
            SET item_name = ?, name = ?, description = ?, category = ?
            WHERE id = ?
        ''', (item_name, name, description, category, id))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))

    return render_template('update.html', item=item, categories=categories)


@app.route('/admin/delete/<int:id>', methods=['POST', 'GET'])
def delete_item(id):
    conn = get_db_connection()

    item = conn.execute('SELECT image_filename FROM items WHERE id = ?', (id,)).fetchone()
    image_path = os.path.join(UPLOAD_FOLDER, item['image_filename'])

    if os.path.exists(image_path):
        os.remove(image_path)

    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def get_db_connection():
    db_path = os.path.join('Final', 'WBHSLostProperty.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == '__main__':
    # init_db()
    app.run(debug=True)




    