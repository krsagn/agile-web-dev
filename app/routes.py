import os
from flask import Blueprint, render_template, request, redirect, url_for, session, abort, flash
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from werkzeug.security import generate_password_hash

from .db import save_login_credentials, save_registered_user

main = Blueprint('main', __name__)

GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "327860289516-5pnn1vlr17acsttkv8miat03hsl40ahd.apps.googleusercontent.com"
)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def test():
    return render_template('test-page.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both your username and password.', 'danger')
            return render_template('login.html'), 400

        password_hash = generate_password_hash(password)
        save_login_credentials(username, password_hash)
        session['user'] = {'username': username}
        flash('Login details saved successfully.', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms_read = request.form.get('terms_read', 'no')

        required_fields = [first_name, last_name, email, username, password, confirm_password]
        if not all(required_fields):
            flash('Please complete all registration fields.', 'danger')
            return render_template('register.html'), 400

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html'), 400

        if terms_read != 'yes':
            flash('Please read and accept the terms before creating an account.', 'danger')
            return render_template('register.html'), 400

        password_hash = generate_password_hash(password)
        save_registered_user(
            first_name,
            last_name,
            email,
            username,
            password_hash,
            terms_read,
        )
        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')

@main.route('/auth/google', methods=['POST'])
def auth_google():
    csrf_cookie = request.cookies.get("g_csrf_token")
    csrf_body = request.form.get("g_csrf_token")

    if not csrf_cookie or not csrf_body or csrf_cookie != csrf_body:
        abort(400, "Invalid CSRF token.")

    credential = request.form.get("credential")
    if not credential:
        abort(400, "Missing Google credential.")

    try:
        idinfo = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except ValueError:
        abort(400, "Invalid Google token.")

    google_sub = idinfo["sub"]
    email = idinfo.get("email")
    name = idinfo.get("name", "")

    # TODO: find or create your local user here
    session["user"] = {
        "google_sub": google_sub,
        "email": email,
        "name": name,
    }

    return redirect(url_for("main.index"))
