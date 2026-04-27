import os
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

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

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
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
