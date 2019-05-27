"""init for app"""
import os

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

from config import Config



APP = Flask(__name__)
APP.config['SESSION_TYPE'] = 'filesystem'
#app.config['SERVER_NAME'] = 'localhost.'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
Session(APP)
MIGRATE = Migrate(APP, DB)
APP.debug = True


from app.server import routes
from app.client import client_routes
