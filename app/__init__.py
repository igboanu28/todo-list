from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from config import Config
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
# from flask_mysqldb import MySQL
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
# app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:Uche_123@localhost/todo_app'
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap5(app)
login = LoginManager(app)
login.login_view = 'login'
login.login_message =('Please log in to access this page')


if not app.debug:

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/todo.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Uche startup')
from app import routes, models, errors