import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config
from sqlalchemy import create_engine
import pyodbc
import urllib.parse

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    params = urllib.parse.quote_plus(
        "DRIVER={ODBC Driver 17 for SQL Server};" +
        "SERVER=tcp:fau-se.database.windows.net,1433;" +
        "DATABASE=FAUSELOGVIEWER;" +
        "UID=fause;" +
        "PWD=esuaf123!@#;" + 
        "Connection Timeout=30"
        )
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" %params
    app.config['SECRET_KEY'] = 'supersecret'
    print('connection is ok')
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/LogView.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('LogView startup')

    return app


from app import models