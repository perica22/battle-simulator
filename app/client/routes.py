import requests
import random
import json
from flask import request, make_response, session, redirect, url_for

from app import app

headers = {"Content-Type": "application/json"}

@app.route('/client2', methods=['GET', 'POST'])
def client2():
    # method for joinging the game / not used after that 
    data = {
        "name":"perica2",
        "number_squads": 50,
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


@app.route('/client3', methods=['GET', 'POST'])
def client3():
    # method for joinging the game / not used after that 
    data = {
        "name":"perica3",
        "number_squads": 100,
        "webhook_url": "http://127.0.0.1:5000/client3/webhook"
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



@app.route('/client3/webhook', methods=['GET', 'POST'])
def client3_webhook():
    # attack strategy: Lower number of squads
    print(session.get('joined_armys_client3'))
    if session.get('joined_armys_client3'):
        import ipdb
        ipdb.set_trace()
    rj = request.get_json()['army']
    if 'joined_armys' not in session or rj['number_squads'] < session['joined_armys']:
        session['joined_armys_client3'] = rj

    print(session.get('joined_armys_client3', None))
    #army_to_attack = random.choice([army['number_squads'] for army in joined_armys])
    if session.get('joined_armys_client3')['number_squads'] < 100:
        #import ipdb
        #ipdb.set_trace()
        #redirect for attack
        return redirect(url_for('client3_attack'))

    # TODO what in case when i don't want to attack ? ? ? ?


@app.route('/client3/attack', methods=['GET', 'POST'])
def client3_attack():
    #attack
    data = {
        "name":"perica3",
        "number_squads": 100
    }
    url ='http://127.0.0.1:5000/starwars/api/attack/{}'.format(session.get('joined_armys_client3')['id'])

    response = requests.put(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return 'success'
    else:
        return 'failure'


