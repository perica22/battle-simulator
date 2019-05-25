import json
import random
import requests
import time

from app import app
from flask import request, make_response, session, redirect, url_for
from app.utils import client_3, client_2, HEADERS, JOIN_URL



@app.route('/client2', methods=['GET', 'POST'])
def client2():
    # method for joinging the game / not used after that
    response = requests.post(
        JOIN_URL, data=json.dumps(client_2.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        client_2.set_access_token(army['access_token'])
        client_2.set_army_id(army['id'])
        time.sleep(5.0)
        return access_token
    else:
       print('-------------nije uspesno-------------')


@app.route('/client3', methods=['GET', 'POST'])
def client3():
    # method for joinging the game / not used after that 
    response = requests.post(
        JOIN_URL, data=json.dumps(client_3.__dict__), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        client_3.set_access_token(army['access_token'])
        client_3.set_army_id(army['id'])
        return redirect(url_for('client2'))
    else:
        print('-------------nije uspesno-------------')


@app.route('/client2/webhook', methods=['POST'])
def client2_webhook():
    # attack strategy: Strongest (highest number of squads)
    joined_armys = []
    rj = request.get_json()

    joined_armys.append(rj['army'])

    #army_to_attack = max([army['number_squads'] for army in joined_armys])

    #redirect for attack
    response = make_response(json.dumps(rj), 200)
    return response

@app.route('/client3/webhook', methods=['GET', 'POST'])
def client3_webhook():
    '''
        - route for receiving webhooks 
        - redirects to /attack route 
        - attack strategy: Lower number of squads
    '''
    if request.headers['Webhook-Topic'] == 'army.update':
        import ipdb
        ipdb.set_trace()
    print('joined_armys_client3' in session)
    if 'joined_armys_client3' in session:
        import ipdb
        ipdb.set_trace()
    rj = request.get_json()['army']
    if 'joined_armys' not in session or rj['number_squads'] < session['joined_armys']:
        session['joined_armys_client3'] = rj


    # TODO create StrategyService instead of redirecting 
    return redirect(url_for('client3_strategy'))

@app.route('/client3/strategy', methods=['GET'])
def client3_strategy():
    print('joined_armys_client3' in session)

    if 'joined_armys_client3' in session and session.get('joined_armys_client3')['number_squads'] < 15:
        #redirect for attack
        return redirect(url_for('client3_attack'))

    # TODO what in case when i don't want to attack ? ? ? ?

@app.route('/client3/attack', methods=['GET', 'POST'])
def client3_attack():
    '''
        - attack route
        - TODO: need to figure out what in case of success
    '''
    #client = request.args.get('client')
    data = {
        "name":client_3.name,
        "number_squads": client_3.number_squads
    }
    url ='http://127.0.0.1:5000/starwars/api/attack/{}?accessToken={}'.format(
        session.get('joined_armys_client3')['id'], access_tokens['client3'])
    print(url)

    response = requests.put(url, data=json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        return 'success'
    else:
        return 'failure'


