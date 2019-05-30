"""
help functions for client
"""
HEADERS = {"Content-Type": "application/json"}
JOIN_URL = 'http://127.0.0.1:5000/starwars/api/join'


class Client():
    """
    - Hardcoded data for clients
    - Using class instead of sessions
    """
    def __init__(self, name, number_squads, webhook_url):
        self.name = name
        self.number_squads = number_squads
        self.webhook_url = webhook_url
        self.status = 'alive'
        self.access_token = None
        self.army_id = None
        self.enemies = []

    def __repr__(self):
        return '<{} data>'.format(self.name)

    def set_access_token_and_id(self, army):
        """Setting access_token after server response"""
        self.access_token = army['accessToken']
        self.army_id = army['id']

    def army_enemie_set(self, payload):
        '''Adding new enemie after army.join webhhok is triggered'''
        enemie = {}
        enemie['id'] = payload['armyId']
        enemie['number_squads'] = payload['squadsCount']
        enemie['type_of_join'] = payload['TypeOfJoin']

        self.enemies.append(enemie)

    def army_enemies_set(self, payload):
        '''Adding all enemies after army.join webhhok is triggered'''
        for army in payload:
            enemie = {}
            enemie['id'] = army['armyId']
            enemie['number_squads'] = army['squadsCount']
            enemie['type_of_join'] = army['TypeOfJoin']

            self.enemies.append(enemie)

    def army_enemies_leave(self, payload):
        '''Removing enemie after army.leave webhhok is triggered'''
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                number = self.enemies.index(army)
                self.enemies.pop(number)
                break

    def army_enemies_update(self, payload):
        '''Updating enemie after army.update webhhok is triggered'''
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                army['number_squads'] = payload['squadsCount']

    def self_update(self, payload):
        '''Self update after army.update webhook is triggered'''
        if payload['squadsCount'] == 0:
            self.status = 'dead'
        self.number_squads = payload['squadsCount']


CLIENT_1 = Client('client1', 45, "http://127.0.0.1:5000/client1/webhook")
CLIENT_2 = Client('client2', 89, "http://127.0.0.1:5000/client2/webhook")
CLIENT_3 = Client('client3', 98, "http://127.0.0.1:5000/client3/webhook")
CLIENT_4 = Client('client4', 36, "http://127.0.0.1:5000/client4/webhook")
CLIENT_5 = Client('client5', 65, "http://127.0.0.1:5000/client5/webhook")
