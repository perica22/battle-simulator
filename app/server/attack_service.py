import random

from flask import session
from sqlalchemy.orm import sessionmaker
from app import db
from app.server.models import Battle
from app.server.webhooks import WebhookService



class AttackService:
    
    def __init__(self, attack_army, defence_army):
        self.attack_army = attack_army
        self.defence_army = defence_army
        self.num_of_attacks = 0

        self.lucky_value = 10#random.randint(1, 15)
        # needs to be (range(1, 101), 100)
        self.array = random.sample(range(1, 15), 10)

    def __enter__(self):
        self.num_of_attacks += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def create(self):
        battle = Battle(attack_army_id=self.attack_army.id,
            defence_army_id=self.defence_army.id,
            attack_army_name=self.attack_army.name,
            defence_army_name=self.defence_army.name,
            defence_army_number_squads=self.defence_army.number_squads,
            num_of_attacks=self.num_of_attacks,
            )
        db.session.add(battle)
        # not sure how to handle session *(READ)*
        return battle

    def attack(self, battle):
        if battle.num_of_attacks >= self.attack_army.number_squads:
            return jsonify({"error": "your reched the max num of attacks"}), 400

        attack_value = 10#random.randint(1,15)
        if attack_value in self.array:
            attack_damage = round(self.attack_army.number_squads / self.num_of_attacks)
            if attack_damage > battle.defence_army_number_squads:
                attack_damage = battle.defence_army_number_squads

            db.session.query(Battle).update({
                Battle.defence_army_number_squads: battle.defence_army_number_squads - attack_damage})
            battle.change_army_number_squads(self.defence_army)
            db.session.commit()

            webhook_service = WebhookService(topic='army.update')
            # triggering army.update webhook
            webhook_service.create_army_update_dead_webhook(self.defence_army)
            webhook_service.create_army_update_alive_webhook(self.defence_army)

            redirect_url = self._build_url_redirect()
            return redirect_url
        else:
            return 'try again'

    def _build_url_redirect(self):
        return "{}_strategy".format(self.attack_army.name)
