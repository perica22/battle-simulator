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
    access_token = db.Column(db.String(120), default=lambda:generate_hash(), unique=True)
    status = db.Column(db.String(64), default='alive')
    join_type = db.Column(db.String(64), default='new')

    def __repr__(self):
        return '<Army {}>'.format(self.name)


class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attack_army_id = db.Column(db.Integer)
    attack_army_name = db.Column(db.String(64))
    defence_army_id = db.Column(db.Integer)
    defence_army_name = db.Column(db.String(64))
    defence_army_number_squads = db.Column(db.Integer)
    attack_army_number_squads = db.Column(db.Integer)
    num_of_attacks = db.Column(db.Integer)

    def __repr__(self):
        return '<Battle {} - {}'.format(self.attack_army_name, self.defence_army_name)

    def change_army_number_squads(self, defense_army):
        defense_army.number_squads = self.defence_army_number_squads
