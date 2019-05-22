from app import db
import os
from uuid import uuid1

def generate_hash():
    hash = str(uuid1())
    return hash

class Army(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    number_squads = db.Column(db.Integer)
    webhook_url = db.Column(db.String(120))
    access_token = db.Column(db.String(120), default=generate_hash(), unique=True)
    status = db.Column(db.String(64), default='alive')
    join_type = db.Column(db.String(64), default='new')

    def __repr__(self):
        return '<Army {}>'.format(self.name)
