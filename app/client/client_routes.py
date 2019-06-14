"""
CLIENT app
"""
import json
import requests

from flask import request

from app import APP
from app.client.utils import Client, HEADERS, JOIN_URL



CLIENTS = []

@APP.route('/<client>', methods=['POST'])
def client(client):
    """
    Method for joinging the game / not used after that
    """
    request_json = request.get_json()
    data = {"name": request_json['name'],
            "number_squads": request_json['number_squads'],
            "webhook_url": request_json['webhook_url']}

    # Making instance of Client
    client = Client(request_json['name'],
                    request_json['number_squads'],
                    request_json['client_strategy'])

    global CLIENTS # global var for keeping track of all joined clients
    CLIENTS.append(client)

    response = requests.post(
        JOIN_URL, data=json.dumps(data), headers=HEADERS)
    if response.status_code == 200:
        army = response.json()['army']
        client.set_access_token_and_id(army)
        return '', 204
    else:
        return '', 400

@APP.route('/<client_name>/webhook', methods=['POST'])
def client_webhook(client_name):
    '''
    Route for receiving webhooks 
    '''
    #finding the right instance of client
    client = [army for army in CLIENTS if army.name == client_name][0]
    request_json = request.get_json()

    if request.headers['Webhook-Topic'] == 'army.join':
        if 'army' in request_json:
            client.army_enemie_set(request_json['army'])
            if client.status == 'alive' and client.enemies:
                client.client_strategy()
            return '', 200
        else:
            client.army_enemies_set(request_json['armies'])
            if client.status == 'alive' and client.enemies:
                client.client_strategy()            
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.update':
        if request_json['army']['armyId'] == client.army_id:
            client.self_update(request_json['army'])
            if client.status == 'alive' and client.enemies:
                client.client_strategy()
            return '', 200
        else:
            client.army_enemies_update(request_json['army'])
            if client.status == 'alive' and client.enemies:
                client.client_strategy()
            return '', 200
    elif request.headers['Webhook-Topic'] == 'army.leave':
        client.army_enemies_leave(request_json['army'])
        return '', 200
