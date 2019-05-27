"""Application model database"""
from uuid import uuid1

from app import DB



def generate_hash():
    '''
    This is generating hash for Army model
    '''
    token_hash = str(uuid1())
    return token_hash


class Army(DB.Model):
    """
    Army table model
    """
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True, unique=True)
    name = DB.Column(DB.String(64))
    number_squads = DB.Column(DB.Integer)
    webhook_url = DB.Column(DB.String(120))
    access_token = DB.Column(DB.String(120), default=lambda: generate_hash(), unique=True)
    status = DB.Column(DB.String(64), default='alive')
    join_type = DB.Column(DB.String(64), default='new')

    def __repr__(self):
        return '<Army {}>'.format(self.name)

    def leave(self, leave_type):
        """changing status of army"""
        self.status = leave_type

    def join_type_update(self):
        """changing join_type of army"""
        self.join_type = 'returned'

class Battle(DB.Model):
    """
    Battle table model
    """
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    attack_army_id = DB.Column(DB.Integer)
    attack_army_name = DB.Column(DB.String(64))
    defence_army_id = DB.Column(DB.Integer)
    defence_army_name = DB.Column(DB.String(64))
    defence_army_number_squads = DB.Column(DB.Integer)
    attack_army_number_squads = DB.Column(DB.Integer)
    num_of_attacks = DB.Column(DB.Integer)

    def __repr__(self):
        return '<Battle {} - {}'.format(self.attack_army_name, self.defence_army_name)

    def change_army_number_squads(self, defense_army):
        """changing number of squads for army"""
        defense_army.number_squads = self.defence_army_number_squads
        if defense_army.number_squads == 0:
            defense_army.status = 'dead'
