from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def test():
<<<<<<< Updated upstream
    return render_template('test-page.html')
=======
    return render_template('test-page.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/results')
def results():
    return render_template('results.html')

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
>>>>>>> Stashed changes
