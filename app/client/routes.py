import requests
import json
from flask import request, make_response

from app import app


@app.route('/client4', methods=['GET', 'POST'])
def client1():
    if request.method == 'GET':
        headers = {"Content-Type": "application/json"}

        data = {
            "name":"perica4",
            "number_squads": 78,
            "webhook_url": "http://127.0.0.1:5000/client4"
        }
        url ='http://127.0.0.1:5000/starwars/api/join'

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            access_token = response.json()['army']['access_token']
            print(access_token)
            return access_token
        else:
            print('nije uspesno') 
    else:
        rj = request.get_json()
        response = make_response(json.dumps(rj), 200)
        print(rj)
        return response
