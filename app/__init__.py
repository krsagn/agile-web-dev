from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'daily_quiz.sqlite3')

    csrf.init_app(app)

    from .db import init_db
    init_db(app)

    from .routes import main
    app.register_blueprint(main)

    return app
