from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # TODO: load from env var before going to prod

    from .routes import main
    app.register_blueprint(main)

    return app

GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "327860289516-5pnn1vlr17acsttkv8miat03hsl40ahd.apps.googleusercontent.com"
)