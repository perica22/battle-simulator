from functools import wraps

from flask import request, jsonify

from app.server.models import Army



HEADERS = {"Content-Type": "application/json"}
JOIN_URL = 'http://127.0.0.1:5000/starwars/api/join'


def generate_hash():
    '''
    This is generating hash for Army model
    '''
    hash = str(uuid1())
    return hash

def check_army_access_token(f):
    """
    This is the decorator checking access token.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.args.get('accessToken')
        attack_army = Army.query.filter_by(
            access_token=access_token).first()
        if attack_army is None:
            return jsonify({"error": "invalid access_token"}), 404
        return f(attack_army, **kwargs)
    return decorated

# using class repr instead of sessions
class Client():
    def __init__(self, name, number_squads, webhook_url):
        self.name = name
        self.number_squads = number_squads
        self.webhook_url = webhook_url

    def __repr__(self):
        return '<{} data>'.format(name)

    def set_access_token(self, access_token):
        self.access_token = access_token
        return

    def set_army_id(self, army_id):
        self.army_id = army_id
        return

client_2 = Client('client2', 10, "http://127.0.0.1:5000/client2/webhook")
client_3 = Client('client3', 15, "http://127.0.0.1:5000/client3/webhook")

#army_to_attack = random.choice([army['number_squads'] for army in joined_armys])