"""
CLIENT_4 app
"""
import json, random, requests

from flask import request

from app import APP
from app.utils import CLIENT_4, HEADERS, JOIN_URL



@APP.route('/client4', methods=['GET', 'POST'])
def client4():
    """
    Method for joinging the game / not used after that
    """
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_4.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_4.set_access_token_and_id(army)
        return '', 204
    else:
        return '', 400

@APP.route('/client4/webhook', methods=['POST'])
def client4_webhook():
    '''
    Route for receiving webhooks 
    '''
    request_json = request.get_json()

    if request.headers['Webhook-Topic'] == 'army.join':
        if 'army' in request_json:
            CLIENT_4.army_enemie_set(request_json['army'])
            if CLIENT_4.status == 'alive':
                client4_strategy()
            return '', 200
        else:
            CLIENT_4.army_enemies_set(request_json['armies'])
            if CLIENT_4.status == 'alive':
                client4_strategy()            
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['army']['armyId'] == CLIENT_4.army_id:
            CLIENT_4.self_update(request_json['army'])
            if CLIENT_4.status == 'alive':
                client4_strategy()
            return '', 200
        else:
            CLIENT_4.army_enemies_update(request_json['army'])
            if CLIENT_4.status == 'alive':
                client4_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.leave':
        CLIENT_4.army_enemies_leave(request_json['army'])
        return '', 200

def client4_strategy():
    """
    Defines the strategy
    Makes a call to attack
    """
    if CLIENT_4.enemies and CLIENT_4.access_token:
        army_to_attack = random.choice(
            [army for army in CLIENT_4.enemies if army['number_squads'] > 0])

        #redirect for attack
        data = {"name":CLIENT_4.name,
                "number_squads": CLIENT_4.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army_to_attack['id'], CLIENT_4.access_token)

        response = requests.put(url, data=json.dumps(data), headers=HEADERS)
        if response.status_code == 400:
            print('{} is WAITING FOR BATTLE TO FINISH'.format(CLIENT_4.name))
    if not CLIENT_4.enemies:
        print('NO ARMIES TO ATTACK')
