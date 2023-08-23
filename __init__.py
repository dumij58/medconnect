import os
# import secrets
from flask import Flask


def create_app():
    # Create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        # Flask
        # SECRET_KEY = secrets.token_hex(),
        SECRET_KEY = "test",

        # Flask-SQLAlchemy
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'medconnect.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,

        # Flask-Mail
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 465,
        MAIL_USERNAME = 'dumij58.medconnect@gmail.com',
        MAIL_PASSWORD = 'wqrpdgsdbmagtyyi',
        MAIL_USE_SSL = True,
        MAIL_DEFAULT_SENDER = ("MedConnect Support","dumij58.medconnect@gmail.com")
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize SQLAlchemy and Flask-Migrate
    from .models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    # Initialize Flask-Mail
    from .email import mail
    mail.init_app(app)

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
    app.jinja_env.filters['age'] = helpers.f_age
    app.jinja_env.filters['dr'] = helpers.f_dr
    app.jinja_env.filters['datetime'] = helpers.f_datetime
    app.jinja_env.filters['dtNoS'] = helpers.f_dtNoS
    app.jinja_env.filters['dtNoSwDay'] = helpers.f_dtNoS_wDay
    app.jinja_env.filters['date'] = helpers.f_date
    app.jinja_env.filters['time'] = helpers.f_time
    app.jinja_env.filters['noSeconds'] = helpers.f_timeNoS
    app.jinja_env.filters['mins'] = helpers.f_mins
    
    return app