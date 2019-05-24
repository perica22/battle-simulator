import random

from flask import session
from sqlalchemy.orm import sessionmaker
from app import db
from app.server.models import Battle



class AttackService:
    
    def __init__(self, attack_army, defense_army):
        self.attack_army = attack_army
        self.defense_army = defense_army
        self.num_of_attacks = 1

        self.lucky_value = random.randint(1, 15)
        # needs to be (range(1, 101), 100)
        self.array = random.sample(range(1, 15), 10)


    def __enter__(self):
        self.num_of_attacks += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def create(self):
        battle = Battle(attack_army_id=self.attack_army.id,
            defence_army_id=self.defense_army.id,
            attack_army_name=self.attack_army.name,
            defence_army_name=self.defense_army.name,
            defence_army_number_squads=self.defense_army.number_squads,
            num_of_attacks=self.num_of_attacks,
            )
        db.session.add(battle)
        # not sure how to handle session *(READ)*
        return battle

    def attack(self, battle):
        if battle.num_of_attacks >= self.attack_army.number_squads:
            return jsonify({"error": "your reched the max num of attacks"}), 400

        attack_value = random.randint(1,15)
        if attack_value in self.array:
            attack_damage = self.attack_army.number_squads / self.num_of_attacks
            self.defense_army.number_squads = self.defense_army.number_squads - attack_damage

            db.session.query(Battle).update({
                Battle.defence_army_number_squads: battle.defence_army_number_squads - attack_damage})
            battle.change_army_number_squads(self.defense_army)
            db.session.commit()
            import ipdb
            ipdb.set_trace()
            redirect_url = self.build_url_redirect()
            return redirect_url
        else:
            return 'try again'

    def build_url_redirect(self):
        return "{}_strategy".format(self.attack_army.name)