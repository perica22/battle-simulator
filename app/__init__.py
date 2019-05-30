"""
init for app
"""
import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config



LOG = logging.getLogger('werkzeug')
LOG.setLevel(logging.ERROR)

APP = Flask(__name__)
APP.config['SESSION_TYPE'] = 'filesystem'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)


from app.server import routes
from app.client import client_routes
