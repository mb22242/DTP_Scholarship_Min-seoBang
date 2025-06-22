from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
SECRET_KEY = os.getenv("SECRET_KEY")


app = Flask(__name__)
app.secret_key = SECRET_KEY


# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User class representing the single admin
class AdminUser(UserMixin):
    id = 1
    username = ADMIN_USERNAME


@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return AdminUser()
    return None


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            login_user(AdminUser())
            return redirect(url_for('admin'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))