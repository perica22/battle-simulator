"""
CLIENT_1 app
"""
import json, random, requests

from flask import request

from app import APP
from app.utils import CLIENT_1, HEADERS, JOIN_URL



@APP.route('/client1', methods=['GET', 'POST'])
def client1():
    """
    Method for joinging the game / not used after that
    """
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_1.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_1.set_access_token_and_id(army)
        return '', 204
    else:
        return '', 400

@APP.route('/client1/webhook', methods=['POST'])
def client1_webhook():
    '''
    Route for receiving webhooks 
    '''
    request_json = request.get_json()

    if request.headers['Webhook-Topic'] == 'army.join':
        if 'army' in request_json:
            CLIENT_1.army_enemie_set(request_json['army'])
            if CLIENT_1.status == 'alive':
                client1_strategy()
            return '', 200
        else:
            CLIENT_1.army_enemies_set(request_json['armies'])
            if CLIENT_1.status == 'alive':
                client1_strategy()            
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['army']['armyId'] == CLIENT_1.army_id:
            CLIENT_1.self_update(request_json['army'])
            if CLIENT_1.status == 'alive':
                client1_strategy()
            return '', 200
        else:
            CLIENT_1.army_enemies_update(request_json['army'])
            if CLIENT_1.status == 'alive':
                client1_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.leave':
        CLIENT_1.army_enemies_leave(request_json['army'])
        return '', 200

def client1_strategy():
    """
    Defines the strategy
    Makes a call to attack
    """
    if CLIENT_1.enemies and CLIENT_1.access_token:
        army_to_attack = random.choice([army for army in CLIENT_1.enemies])
        #redirect for attack
        data = {"name":CLIENT_1.name,
                "number_squads": CLIENT_1.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army_to_attack['id'], CLIENT_1.access_token)

        response = requests.put(url, data=json.dumps(data), headers=HEADERS)
        if response.status_code == 400:
            print('SERVER REPLY:{}'.format(response.json()['error']))
