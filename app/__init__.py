from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session



app = Flask(__name__)
#app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#Session(app)


from app.server import routes, models
from app.client import routes
