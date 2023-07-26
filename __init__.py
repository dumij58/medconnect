import os
import secrets

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

def create_app():
    # Create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY = secrets.token_hex(),
        SECRET_KEY = "test",
        # DATABASE=os.path.join(app.instance_path, 'medconnect.sqlite'),
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'medconnect.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    return app