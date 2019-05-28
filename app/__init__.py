"""
init for app
NEGDE NEKI THREAD FALI
TRENUTNO BLOKER TO STO SE NE NAPRAVE SVE ARMIJE
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config



APP = Flask(__name__)
APP.config['SESSION_TYPE'] = 'filesystem'
#app.config['SERVER_NAME'] = 'localhost.'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)
APP.debug = True


from app.server import routes
from app.client1 import client1_routes
from app.client2 import client2_routes
from app.client3 import client3_routes
