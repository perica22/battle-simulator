import requests
import json


headers = {"Content-Type": "application/json"}

data = {
        "name":"perica2",
        "number_squads": 50,
        "webhook_url": "http://127.0.0.1:5000/client2/webhook"
    }
url ='http://127.0.0.1:5000/starwars/api/join'

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
	data = {
	        "name":"perica3",
	        "number_squads": 100,
	        "webhook_url": "http://127.0.0.1:5000/client3/webhook"
	    }
	url ='http://127.0.0.1:5000/starwars/api/join'

	response = requests.post(url, data=json.dumps(data), headers=headers)