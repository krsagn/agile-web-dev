import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .models import db as sqlalchemy_db

load_dotenv()

csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    sqlalchemy_db.init_app(app)
    migrate.init_app(app, sqlalchemy_db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    from .db import find_registered_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return find_registered_user_by_id(int(user_id))
        except (TypeError, ValueError):
            return None

    return app
