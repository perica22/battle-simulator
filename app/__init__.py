from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SERVER_NAME'] = 'localhost.'
app.config.from_object(Config)
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.debug = True


from app.server import routes, models
from app.client import routes
