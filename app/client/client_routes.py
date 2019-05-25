'''
TODO: 
    - implement /leave route
    - then next think should be client side of game :) 
'''
import json, random, requests, time

from flask import request, make_response, session, redirect, url_for

from app import APP
from app.utils import CLIENT_2, CLIENT_3, HEADERS, JOIN_URL



@APP.route('/client2', methods=['GET', 'POST'])
def client2():
    # method for joinging the game / not used after that
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_2.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_2.set_access_token(army['access_token'])
        CLIENT_2.set_army_id(army['id'])
        time.sleep(10.0)
        return access_token
    else:
       print('-------------nije uspesno-------------')


@APP.route('/client3', methods=['GET', 'POST'])
def client3():
    # method for joinging the game / not used after that 
    response = requests.post(
        JOIN_URL, data=json.dumps(CLIENT_3.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        CLIENT_3.set_access_token(army['access_token'])
        CLIENT_3.set_army_id(army['id'])
        return redirect(url_for('client2'))
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

@APP.route('/client3/webhook', methods=['GET', 'POST'])
def client3_webhook():
    '''
        - route for receiving webhooks 
        - redirects to /attack route 
        - attack strategy: Lower number of squads
    '''
    if request.headers['Webhook-Topic'] == 'army.update':
        pass

    rj = request.get_json()['army']
    if 'joined_armys' not in session or rj['number_squads'] < session['joined_armys']:
        session['joined_armys_client3'] = rj


    # TODO create StrategyService instead of redirecting 
    return redirect(url_for('client3_strategy'))

@APP.route('/client3/strategy', methods=['GET'])
def client3_strategy():
    print('joined_armys_client3' in session)

    if 'joined_armys_client3' in session and session.get('joined_armys_client3')['number_squads'] < 15:
        #redirect for attack
        return redirect(url_for('client3_attack'))

    # TODO what in case when i don't want to attack ? ? ? ?

@APP.route('/client3/attack', methods=['GET', 'POST'])
def client3_attack():
    '''
        - attack route
        - TODO: need to figure out what in case of success
    '''
    #client = request.args.get('client')
    data = {
        "name":CLIENT_3.name,
        "number_squads": CLIENT_3.number_squads
    }
    url ='http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
        session.get('joined_armys_client3')['id'], CLIENT_3.access_token)
    print(url)

    response = requests.put(url, data=json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        return 'success'
    else:
        return 'failure'


