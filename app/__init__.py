"""init for add"""
import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session



APP = Flask(__name__)
APP.config['SESSION_TYPE'] = 'filesystem'
#app.config['SERVER_NAME'] = 'localhost.'

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(BASEDIR, 'app.db')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)
Session(APP)
MIGRATE = Migrate(APP, DB)
APP.debug = True

from app.server import routes
from app.client import client_routes
