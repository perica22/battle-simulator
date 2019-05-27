"""
CLIENT_3 app
"""
import json, random, requests, time

from flask import request, make_response, session, redirect, url_for

from app import APP
from app.utils import CLIENT_2, CLIENT_3, HEADERS, JOIN_URL



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
        time.sleep(3.0)
        return redirect(url_for('client2'))
    else:
        print('-------------nije uspesno-------------')

@APP.route('/client3/webhook', methods=['POST'])
def client3_webhook():
    '''
    Route for receiving webhooks 
    '''
    request_json = request.get_json()['army']

    if request.headers['Webhook-Topic'] == 'army.join':
        CLIENT_3.army_enemies_set(request_json)
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['armyId'] == CLIENT_3.id:
            CLIENT_3.self_update(request_json)
        else:
            CLIENT_3.army_enemies_update(request_json)
    elif request.headers['Webhook-Topic'] == 'army.leave':
        CLIENT_3.army_enemies_leave(request_json)

    # TODO create StrategyService instead of redirecting 
    return redirect(url_for('client3_strategy'))

@APP.route('/client3/strategy', methods=['GET'])
def client3_strategy():
    """
    Defines the strategy
    Makes a call to attack
    """
    if CLIENT_3.join_battle == False:
        attack_army = None
        for army in CLIENT_3.enemies:
            if attack_army and army['number_squads'] < attack_army:
                attack_army = army['id']
            else:
                attack_army = army['id']

        #redirect for attack
        data = {"name":CLIENT_3.name,
                "number_squads": CLIENT_3.number_squads}
        url = 'http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
            army, CLIENT_3.access_token)

        CLIENT_3.battle_status()
        response = requests.put(url, data=json.dumps(data), headers=HEADERS)

        if response.status_code:
            CLIENT_3.battle_status()
            return '', 204
    else:
        print('{} is WAITING FOR BATTLE TO FINISH'.format(CLIENT_3.name))
        return '', 204

'''
@APP.route('/client3/attack', methods=['GET', 'POST'])
def client3_attack():
 
    army=request.args.get('army_id')
'''    





@APP.route('/client2', methods=['GET', 'POST'])
def client2():
    # method for joinging the game / not used after that
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_2.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_2.set_access_token_and_id(army)
        print("all armys have joined")
        time.sleep(10.0)
        return "all armys have joined"
    else:
       print('-------------nije uspesno-------------')

@APP.route('/client2/webhook', methods=['POST'])
def client2_webhook():
    # attack strategy: Strongest (highest number of squads)
    joined_armys = []
    rj = request.get_json()

    joined_armys.append(rj['army'])

    #army_to_attack = max([army['number_squads'] for army in joined_armys])

    #redirect for attack
    response = make_response(json.dumps(rj), 200)
    return response
