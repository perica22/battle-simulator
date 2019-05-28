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

    def army_enemie_set(self, payload):
        enemie = {}
        enemie['id'] = payload['armyId']
        enemie['number_squads'] = payload['squadsCount']
        enemie['type_of_join'] = payload['TypeOfJoin']

        self.enemies.append(enemie)

    def army_enemies_set(self, payload):
        for army in payload:
            enemie = {}
            enemie['id'] = army['armyId']
            enemie['number_squads'] = army['squadsCount']
            enemie['type_of_join'] = army['TypeOfJoin']

            self.enemies.append(enemie)

    def army_enemies_leave(self, payload):
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                #army['type_of_leave'] = payload['TypeOfLeave']
                number = self.enemies.index(army)
                self.enemies.pop(number)
                break

    def army_enemies_update(self, payload):
        for army in self.enemies:
            if army['id'] == payload['armyId']:
                army['number_squads'] = payload['squadsCount']
                army['rank_rate'] = payload['rankRate']

    def self_update(self, payload):
        self.rank_rate = payload['rankRate']
        self.number_squads = payload['squadsCount']


CLIENT_1 = Client('client1', 70, "http://127.0.0.1:5000/client1/webhook")
CLIENT_2 = Client('client2', 90, "http://127.0.0.1:5000/client2/webhook")
CLIENT_3 = Client('client3', 80, "http://127.0.0.1:5000/client3/webhook")
CLIENT_4 = Client('client4', 60, "http://127.0.0.1:5000/client4/webhook")
CLIENT_5 = Client('client5', 88, "http://127.0.0.1:5000/client5/webhook")
