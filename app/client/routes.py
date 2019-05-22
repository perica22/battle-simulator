import requests
import json
from flask import request

from app import app


@app.route('/client6', methods=['GET', 'POST'])
def client1():
    if request.method == 'GET':
        headers = {"Content-Type": "application/json"}

        data = {
            "name":"perica6",
            "number_squads": 78,
            "webhook_url": "http://127.0.0.1:5000/client6"
        }
        url ='http://127.0.0.1:5000/starwars/api/join'

        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            access_token = resoponse.json()['army']['access_token']
        else:
            print('nije uspesno') 


    else:
        import ipdb
        ipdb.set_trace()
        print('asdasd')
