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
        self.army_id = None

    def __repr__(self):
        return '<{} data>'.format(self.name)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def set_army_id(self, army_id):
        self.army_id = army_id

CLIENT_2 = Client('client2', 10, "http://127.0.0.1:5000/client2/webhook")
CLIENT_3 = Client('client3', 15, "http://127.0.0.1:5000/client3/webhook")

#army_to_attack = random.choice([army['number_squads'] for army in joined_armys])
