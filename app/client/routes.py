import requests
import random
import json
from flask import request, make_response, session, redirect, url_for

from app import app

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/client1', methods=['GET', 'POST'])
def client1():
    # method for joinging the game / not used after that 

    headers = {"Content-Type": "application/json"}
    data = {
        "name":"perica1",
        "number_squads": 88,
        "webhook_url": "http://127.0.0.1:5000/client1/webhook"
    }
    url ='http://127.0.0.1:5000/starwars/api/join'
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        access_token = response.json()['army']['access_token']
        print(access_token)
        #return access_token
        return redirect(url_for('client2'))
    else:
        print('-------------nije uspesno-------------')


@app.route('/client1/webhook', methods=['POST'])
def client1_webhook():
    # attack strategy: Weakest (lowest number of squads)
    joined_armys = []
    rj = request.get_json()
    joined_armys.append(rj['army'])

    army_to_attack = min([army['number_squads'] for army in joined_armys])
    
    #redirect for attack
    response = make_response(json.dumps(rj), 200)
    return response


@app.route('/client2', methods=['GET', 'POST'])
def client2():
    # method for joinging the game / not used after that 
    headers = {"Content-Type": "application/json"}
    data = {
        "name":"perica2",
        "number_squads": 66,
        "webhook_url": "http://127.0.0.1:5000/client2/webhook"
    }
    url ='http://127.0.0.1:5000/starwars/api/join'

    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        access_token = response.json()['army']['access_token']
        print(access_token)
        return access_token
    else:
       print('-------------nije uspesno-------------')


@app.route('/client2/webhook', methods=['POST'])
def client2_webhook():
    # attack strategy: Strongest (highest number of squads)
    joined_armys = []
    rj = request.get_json()
    joined_armys.append(rj['army'])

    army_to_attack = max([army['number_squads'] for army in joined_armys])

    #redirect for attack
    response = make_response(json.dumps(rj), 200)
    return response


@app.route('/client3', methods=['GET', 'POST'])
def client3():
    # method for joinging the game / not used after that 
    headers = {"Content-Type": "application/json"}
    data = {
        "name":"perica3",
        "number_squads": 67,
        "webhook_url": "http://127.0.0.1:5000/client3/webhook"
    }
    url ='http://127.0.0.1:5000/starwars/api/join'

    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        access_token = response.json()['army']['access_token']
        print(access_token)
        #return access_token
        return redirect(url_for('client1'))
    else:
        print('-------------nije uspesno-------------')


@app.route('/client3/webhook', methods=['POST'])
def client3_webhook():

    # attack strategy: Random
    print('joined_armys' in session)
    if 'joined_armys' in session:
        import ipdb
        ipdb.set_trace()
    rj = request.get_json()['army']
    if 'joined_armys' not in session or rj['number_squads'] > session['joined_armys']:
        session['joined_armys'] = rj['number_squads']

    #army_to_attack = random.choice([army['number_squads'] for army in joined_armys])
    print(session['joined_armys'])
    # needs to be random number taken from tottal number of armys

    #redirect for attack
    response = make_response(json.dumps(rj), 200)
    return response
