from app import db
import os


class Army(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    number_squads = db.Column(db.Integer)
    webhook_url = db.Column(db.String(120))
    access_token = db.Column(db.String(120))
    status = db.Column(db.String(64), default='alive')
    join_type = db.Column(db.String(64), default='new')

    def __repr__(self):
        return '<Army {}>'.format(self.name)

    def generate_hash(self):
        hash = os.urandom(8)
        return "{}{}".format(self.id, hash)
