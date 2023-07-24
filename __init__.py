import os
import secrets
from flask import Flask

def create_app():
    # Create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY = secrets.token_hex(),
        SECRET_KEY = "test",
        DATABASE=os.path.join(app.instance_path, 'medconnect.sqlite')
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')

    return app