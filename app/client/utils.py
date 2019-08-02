"""
help functions for client
"""
import json
import random
import requests



HEADERS = {"Content-Type": "application/json"}
JOIN_URL = 'http://127.0.0.1:5000/starwars/api/join'

class Client:
    """
    Class for generating new client
    Args:
        name: army name
        number_squads: army number of squads
        army_strategy: defines which armies this client is going to attck
                        (based on max, min, random squad_number or enemies)
    """
    def __init__(self, name, number_squads, army_strategy):
        self.name = name
        self.number_squads = number_squads
        self.army_strategy = army_strategy
        self.status = 'alive'
        self.access_token = None
        self.army_id = None
        self.enemies = []

    def __repr__(self):
        return '<{} data>'.format(self.name)

    def set_access_token_and_id(self, army):
        """
        Setting access_token after server response
        Args:
            army: data received from API response
        """
        self.access_token = army['accessToken']
        self.army_id = army['id']

    def army_enemie_set(self, payload):
        """
        Adding new enemy after army.join webhook is triggered
        Args:
            payload: data received from webhook
        """
        enemie = {}
        enemie['id'] = payload['armyId']
        enemie['number_squads'] = payload['squadsCount']
        enemie['type_of_join'] = payload['TypeOfJoin']

        self.enemies.append(enemie)

    def army_enemies_set(self, payload):
        """
        Adding all enemies after army.join webhook is triggered
        Args:
            payload: data received from webhook
        """
        for army in payload:
            enemie = {}
            enemie['id'] = army['armyId']
            enemie['number_squads'] = army['squadsCount']
            enemie['type_of_join'] = army['TypeOfJoin']

            self.enemies.append(enemie)

    def army_enemies_leave(self, payload):
        """
        Removing enemy after army.leave webhook is triggered
        Args:
            payload: data received from webhook
        """
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                number = self.enemies.index(army)
                self.enemies.pop(number)
                break

    def army_enemies_update(self, payload):
        """
        Updating enemy after army.update webhook is triggered
        Args:
            payload: data received from webhook
        """
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                army['number_squads'] = payload['squadsCount']

    def self_update(self, payload):
        """
        Self update after army.update webhook is triggered
        Args:
            payload: data received from webhook
        """
        if payload['squadsCount'] == 0:
            self.status = 'dead'
        self.number_squads = payload['squadsCount']

    def client_strategy(self):
        """
        Defines the strategy; Makes a call to attack
        """
        if self.army_strategy == "max":
            army_to_attack = self._max_function()
        elif self.army_strategy == "min":
            army_to_attack = self._min_function()
        else:
            army_to_attack = random.choice([army['id'] for army in self.enemies])

        self._attack_call(army_to_attack) # redirect for attack

    def _attack_call(self, army_to_attack):
        """
        Making a call to attack
        Args:
            army_to_attack: army that is choosen to be attacked
        """
        data = {"name":self.name,
                "number_squads": self.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army_to_attack, self.access_token)

        response = requests.put(url, data=json.dumps(data), headers=HEADERS)
        if response.status_code == 400:
            print('SERVER REPLY:{} - {}'.format(self.name, response.json()['error']))
        if response.status_code == 429:
            print('SERVER REPLY:{} - {}'.format(self.name, response.json()['error']))
            self.client_strategy()

    def _min_function(self):
        """
        Retrieving enemy with min squad_number
        Returns:
            army_id of army with min squad_number
        """
        army_id = None
        min_value = None
        for army in self.enemies:
            if not min_value:
                min_value = army['number_squads']
                army_id = army['id']
            elif army['number_squads'] < min_value:
                min_value = army['number_squads']
                army_id = army['id']
        return army_id

    def _max_function(self):
        """
        Retrieving enemy with max squad_number
        Returns:
            army_id of army with max squad_number
        """
        army_id = None
        max_value = None
        for army in self.enemies:
            if not max_value:
                max_value = army['number_squads']
                army_id = army['id']
            elif army['number_squads'] > max_value:
                max_value = army['number_squads']
                army_id = army['id']
        return army_id
