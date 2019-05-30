"""
CLIENT_3 app
"""
import json, random, requests

from flask import request

from app import APP
from app.utils import CLIENT_3, HEADERS, JOIN_URL



@APP.route('/client3', methods=['GET', 'POST'])
def client3():
    """
    Method for joinging the game / not used after that
    """
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_3.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_3.set_access_token_and_id(army)
        return '', 204
    else:
        return '', 400

@APP.route('/client3/webhook', methods=['POST'])
def client3_webhook():
    '''
    Route for receiving webhooks 
    '''
    request_json = request.get_json()

    if request.headers['Webhook-Topic'] == 'army.join':
        if 'army' in request_json:
            CLIENT_3.army_enemie_set(request_json['army'])
            if CLIENT_3.status == 'alive' and CLIENT_3.enemies:
                client3_strategy()
            return '', 200
        else:
            CLIENT_3.army_enemies_set(request_json['armies'])
            if CLIENT_3.status == 'alive' and CLIENT_3.enemies:
                client3_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['army']['armyId'] == CLIENT_3.army_id:
            CLIENT_3.self_update(request_json['army'])
            if CLIENT_3.status == 'alive' and CLIENT_3.enemies:
                client3_strategy()
            return '', 200
        else:
            CLIENT_3.army_enemies_update(request_json['army'])
            if CLIENT_3.status == 'alive' and CLIENT_3.enemies:
                client3_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.leave':
        CLIENT_3.army_enemies_leave(request_json['army'])
        return '', 200

def client3_strategy():
    """
    Defines the strategy
    Makes a call to attack
    """
    if CLIENT_3.enemies and CLIENT_3.access_token:
        armies_to_attack = [army for army in CLIENT_3.enemies]
        army_to_attack = max_function(armies_to_attack)

        #redirect for attack
        data = {"name":CLIENT_3.name,
                "number_squads": CLIENT_3.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army_to_attack, CLIENT_3.access_token)

        response = requests.put(url, data=json.dumps(data), headers=HEADERS)
        if response.status_code == 400:
            print('SERVER REPLY:{}'.format(response.json()['error']))

def max_function(armies_list):
    army_id = None
    max_value = None
    for army in armies_list:
        if not max_value:
            max_value = army['number_squads']
            army_id = army['id']
        elif army['number_squads'] > max_value:
            max_value = army['number_squads']
            army_id = army['id']
    return army_id
