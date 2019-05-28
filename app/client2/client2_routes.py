"""
CLIENT_2 app
"""
import json, random, requests, time, threading

from flask import request, make_response, redirect, url_for

from app import APP
from app.utils import CLIENT_2, HEADERS, JOIN_URL



@APP.route('/client2', methods=['GET', 'POST'])
def client2():
    """
    Method for joinging the game / not used after that
    """    
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_2.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_2.set_access_token_and_id(army)
        return '', 204
    else:
       print('-------------nije uspesno-------------')

@APP.route('/client2/webhook', methods=['POST'])
def client2_webhook():
    '''
    Route for receiving webhooks 
    '''
    request_json = request.get_json()

    if request.headers['Webhook-Topic'] == 'army.join':
        if 'army' in request_json:
            CLIENT_2.army_enemie_set(request_json['army'])
            #q = threading.Thread(
            #    target=client2_strategy)
            #q.start()
            client2_strategy()
            return '', 200
        else:
            CLIENT_2.army_enemies_set(request_json['armies'])
            #t = threading.Thread(
            #    target=client2_strategy)
            #t.start()
            client2_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['army']['armyId'] == CLIENT_2.id:
            CLIENT_2.self_update(request_json['army'])
            client2_strategy()
            return '', 200
        else:
            CLIENT_2.army_enemies_update(request_json['army'])
            #w = threading.Thread(
            #    target=client2_strategy)
            #w.start()
            client2_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.leave':
        CLIENT_2.army_enemies_leave(request_json['army'])
        return '', 200

def client2_strategy():
    """
    Defines the strategy
    Makes a call to attack
    """
    if CLIENT_2.enemies and CLIENT_2.access_token:
        armies_to_attack = [army for army in CLIENT_2.enemies if army['number_squads'] > 0]
        army_to_attack = min_function(armies_to_attack)
        #redirect for attack
        data = {"name":CLIENT_2.name,
                "number_squads": CLIENT_2.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army_to_attack, CLIENT_2.access_token)

        response = requests.put(url, data=json.dumps(data), headers=HEADERS)
        if response.status_code == 400:
            print('{} is WAITING FOR BATTLE TO FINISH'.format(CLIENT_2.name))

    if not CLIENT_2.enemies:
        print('NO ARMIES TO ATTACK')

def min_function(armies_list):
    army_id = None
    min_value = None
    for army in armies_list:
        if not min_value:
            min_value = army['number_squads']
            army_id = army['id']
        elif army['number_squads'] < min_value:
            min_value = army['number_squads']
            army_id = army['id']
    return army_id
