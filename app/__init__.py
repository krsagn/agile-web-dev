import logging
import os

from dotenv import load_dotenv

logging.basicConfig(level=logging.WARNING)
logging.getLogger("app").setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.INFO)
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .models import db as sqlalchemy_db
from .scheduler import scheduler

load_dotenv()

csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)

    sqlalchemy_db.init_app(app)
    migrate.init_app(app, sqlalchemy_db)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    should_run_scheduler = (
        os.environ.get("WERKZEUG_RUN_MAIN") == "true"
        or os.environ.get("RUN_SCHEDULER") == "1"
    )
    if should_run_scheduler:
        scheduler.init_app(app)
        scheduler.start()
        app.logger.info("Scheduler started — %d job(s) registered", len(scheduler.get_jobs()))
    else:
        app.logger.info("Scheduler skipped (WERKZEUG_RUN_MAIN/RUN_SCHEDULER not set)")

    from .seed import seed_command, reset_db_command
    app.cli.add_command(seed_command)
    app.cli.add_command(reset_db_command)

    from .db import find_registered_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return find_registered_user_by_id(int(user_id))
        except (TypeError, ValueError):
            return None

    return app
