import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .models import db

load_dotenv()

csrf = CSRFProtect()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
