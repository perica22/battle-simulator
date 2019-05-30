"""
CLIENT_5 app
"""
import json, random, requests

from flask import request

from app import APP
from app.utils import CLIENT_5, HEADERS, JOIN_URL



@APP.route('/client5', methods=['GET', 'POST'])
def client5():
    """
    Method for joinging the game / not used after that
    """
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_5.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_5.set_access_token_and_id(army)
        return '', 204
    else:
        return '', 400

@APP.route('/client5/webhook', methods=['POST'])
def client5_webhook():
    '''
    Route for receiving webhooks 
    '''
    request_json = request.get_json()

    if request.headers['Webhook-Topic'] == 'army.join':
        if 'army' in request_json:
            CLIENT_5.army_enemie_set(request_json['army'])
            if CLIENT_5.status == 'alive' and CLIENT_5.enemies:
                client5_strategy()
            return '', 200
        else:
            CLIENT_5.army_enemies_set(request_json['armies'])
            if CLIENT_5.status == 'alive' and CLIENT_5.enemies:
                client5_strategy()            
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['army']['armyId'] == CLIENT_5.army_id:
            CLIENT_5.self_update(request_json['army'])
            if CLIENT_5.status == 'alive' and CLIENT_5.enemies:
                client5_strategy()
            return '', 200
        else:
            CLIENT_5.army_enemies_update(request_json['army'])
            if CLIENT_5.status == 'alive' and CLIENT_5.enemies:
                client5_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.leave':
        CLIENT_5.army_enemies_leave(request_json['army'])
        return '', 200

def client5_strategy():
    """
    Defines the strategy
    Makes a call to attack
    """
    if CLIENT_5.enemies and CLIENT_5.access_token:
        army_to_attack = random.choice(
            [army for army in CLIENT_5.enemies])

        #redirect for attack
        data = {"name":CLIENT_5.name,
                "number_squads": CLIENT_5.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army_to_attack['id'], CLIENT_5.access_token)

        response = requests.put(url, data=json.dumps(data), headers=HEADERS)
        if response.status_code == 400:
            print('SERVER REPLY:{}'.format(response.json()['error']))
