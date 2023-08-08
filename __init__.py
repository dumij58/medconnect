import os
# import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        # SECRET_KEY = secrets.token_hex(),
        SECRET_KEY = "test",
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'medconnect.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models
        db.create_all()

    # Import and register blueprints
    from . import auth, admin, main, doc, pt
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(doc.bp)
    app.register_blueprint(pt.bp)

    # Config url rules
    app.add_url_rule('/', endpoint='index')

    # Set up env filters
    from . import helpers
    app.jinja_env.filters['phone_no'] = helpers.f_phone_no
    app.jinja_env.filters['gender'] = helpers.f_gender
    app.jinja_env.filters['hospital'] = helpers.f_hospital
    app.jinja_env.filters['datetime'] = helpers.f_datetime
    app.jinja_env.filters['date'] = helpers.f_date
    app.jinja_env.filters['time'] = helpers.f_time
    app.jinja_env.filters['noSeconds'] = helpers.f_timeNoS

    return app