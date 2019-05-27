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
        self.access_token = None
        self.id = None
        self.rank_rate = None
        self.join_battle = False
        self.enemies = []

    def __repr__(self):
        return '<{} data>'.format(self.name)

    def set_access_token_and_id(self, army):
        """Setting access_token after server response"""
        self.access_token = army['accessToken']
        self.id = army['id']

    def army_enemies_set(self, payload):
        enemie = {}
        enemie['id'] = payload['armyId']
        enemie['number_squads'] = payload['squadsCount']
        enemie['type_of_join'] = payload['TypeOfJoin']

        self.enemies.append(enemie)

    def army_enemies_leave(self, payload):
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                army['type_of_leave'] = payload['TypeOfLeave']

    def army_enemies_update(self, payload):
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                army['number_squads'] = payload['squadsCount']
                army['rank_rate'] = payload['rankRate']

    def self_update(self, payload):
        self.rank_rate = payload['rankRate']
        self.number_squads = payload['squadsCount']

    def battle_status(self):
        self.join_battle = True if self.join_battle == False else False


CLIENT_2 = Client('client2', 10, "http://127.0.0.1:5000/client2/webhook")
CLIENT_3 = Client('client3', 15, "http://127.0.0.1:5000/client3/webhook")

#army_to_attack = random.choice([army['number_squads'] for army in joined_armys])
