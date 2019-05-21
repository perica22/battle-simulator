from app import db


class Army(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    number_squads = db.Column(db.Integer)
    webhook_url = db.Column(db.String(120))

    def __repr__(self):
        return '<Army {}>'.format(self.name)