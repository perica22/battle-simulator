"""Service for handling battle"""
import random
import threading

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

        self.lucky_value = random.randint(1, 5)
        # needs to be (range(1, 101), 100)
        self.array = [1, 2, 3, 4, 5]#random.sample(range(1, 101), 100)#[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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
        """Adding battle to DB"""
        self._set_in_battle_army_status()
        battle = Battle(attack_army_id=self.attack_army.id,
                        defence_army_id=self.defence_army.id,
                        attack_army_name=self.attack_army.name,
                        defence_army_name=self.defence_army.name,
                        defence_army_number_squads=self.defence_army.number_squads,
                        attack_army_number_squads=self.attack_army.number_squads,)
        DB.session.add(battle)
        print("{} battle started".format(battle))

        return battle

    def attack(self, battle):
        """Determining if attack was succesfull"""
        if self.num_of_attacks >= self.attack_army.number_squads:
            self._set_in_battle_army_status()
            return jsonify({"error": "your reched the max num of attacks"}), 400
            
        attack_value = random.randint(1, 5)
        print("lucky_value is {} and army strikes with {}".format(self.lucky_value, attack_value))
        if attack_value == self.lucky_value:
            attack_damage = round(self.attack_army.number_squads / self.num_of_attacks)
            if attack_damage > battle.defence_army_number_squads:
                attack_damage = battle.defence_army_number_squads
                self.dead = True

            self._set_in_battle_army_status()
            self.defence_army.set_defence_army_number_squads(attack_damage)
            ##print('---------', self.attack_army.in_battle)
            #print('---------', self.defence_army.in_battle)

            squad_number = battle.defence_army_number_squads - attack_damage
            DB.session.query(
                Battle).update({
                    Battle.defence_army_number_squads: squad_number})
            battle.change_army_number_squads(self.defence_army)
            DB.session.commit()

            return 'success'

        return 'try_again'

    def trigger_webhooks(self):
        """Triggering webhooks"""
        webhook_service = WebhookService()
        '''x = threading.Thread(
                    target=webhook_service.create_army_update_webhook, args=(self.defence_army,))
        x.start()
        y = threading.Thread(
                    target=webhook_service.create_army_update_webhook, args=(self.attack_army,))
        y.start()'''

        # triggering army.update webhook
        webhook_service.create_army_update_webhook(self.defence_army)
        webhook_service.create_army_update_webhook(self.attack_army)

        # army.leave webhook in case army died
        if self.dead:
            webhook_service.create_army_leave_webhook(self.defence_army, leave_type='die')

    def _set_in_battle_army_status(self):
        self.attack_army.is_in_active_battle()
        self.defence_army.is_in_active_battle()
