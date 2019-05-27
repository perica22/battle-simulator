"""Service for handling battle"""
#import random

from flask import jsonify

from app import DB
from .models import Battle, Army
from .webhooks import WebhookService



class ArmyAttackService:
    """
    Handling battle logic
    """
    def __init__(self, attack_army):
        self.attack_army = attack_army
        self.defence_army = None
        self.num_of_attacks = 0
        self.dead = False

        self.lucky_value = 10#random.randint(1, 15)
        # needs to be (range(1, 101), 100)
        self.array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]#random.sample(range(1, 15), 10)

    def __enter__(self):
        self.num_of_attacks += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_defence_army(self, army_id):
        """Retriving defence army"""
        self.defence_army = Army.query.filter_by(id=army_id).first()
        return self.defence_army

    def create(self):
        """Ddding battle to DB"""
        battle = Battle(attack_army_id=self.attack_army.id,
                        defence_army_id=self.defence_army.id,
                        attack_army_name=self.attack_army.name,
                        defence_army_name=self.defence_army.name,
                        defence_army_number_squads=self.defence_army.number_squads,
                        num_of_attacks=self.num_of_attacks,
                        )
        DB.session.add(battle)
        print("{} battle started".format(battle))
        # not sure how to handle session *(READ)*
        return battle

    def attack(self, battle):
        """Determining if attack was succesfull"""
        if battle.num_of_attacks >= self.attack_army.number_squads:
            return jsonify({"error": "your reched the max num of attacks"}), 400

        attack_value = 10#random.randint(1,15)
        if attack_value in self.array:
            attack_damage = round(self.attack_army.number_squads / self.num_of_attacks)
            if attack_damage > battle.defence_army_number_squads:
                attack_damage = battle.defence_army_number_squads
                self.dead = True

            squad_number = battle.defence_army_number_squads - attack_damage
            DB.session.query(
                Battle).update({
                    Battle.defence_army_number_squads: squad_number})
            battle.change_army_number_squads(self.defence_army)
            DB.session.commit()

            return self._build_url_redirect()

        return 'try_again'

    def trigger_webhooks(self):
        """Triggering webhooks"""
        webhook_service = WebhookService()

        # triggering army.update webhook
        webhook_service.create_army_update_webhook(self.defence_army)
        webhook_service.create_army_update_webhook(self.attack_army)

        # army.leave webhook in case army died
        if self.dead:
            webhook_service.create_army_leave_webhook(self.defence_army, leave_type='die')

    def _build_url_redirect(self):
        """Not sure if this is needed ???"""
        return "{}_strategy".format(self.attack_army.name)
