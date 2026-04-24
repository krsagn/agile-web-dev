from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # TODO: load from env var before going to prod

    from .routes import main
    app.register_blueprint(main)

    return app