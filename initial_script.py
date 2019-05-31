"""INITIAL SCRIPT"""
import json
import time
import requests



HEADERS = {"Content-Type": "application/json"}

DATA = {
    "name":"client1",
    "number_squads": 25,
    "webhook_url": "http://127.0.0.1:5000/client1/webhook",
    "client_strategy": "min"
}
URL = 'http://127.0.0.1:5000/client1'
requests.post(URL, data=json.dumps(DATA), headers=HEADERS)

DATA = {
    "name":"client2",
    "number_squads": 45,
    "webhook_url": "http://127.0.0.1:5000/client2/webhook",
    "client_strategy": "max"
}
time.sleep(3)
URL = 'http://127.0.0.1:5000/client2'
requests.post(URL, data=json.dumps(DATA), headers=HEADERS)

DATA = {
    "name":"client3",
    "number_squads": 65,
    "webhook_url": "http://127.0.0.1:5000/client3/webhook",
    "client_strategy": "random"
}
time.sleep(3)
URL = 'http://127.0.0.1:5000/client3'
requests.post(URL, data=json.dumps(DATA), headers=HEADERS)

DATA = {
    "name":"client4",
    "number_squads": 35,
    "webhook_url": "http://127.0.0.1:5000/client4/webhook",
    "client_strategy": "max"
}
URL = 'http://127.0.0.1:5000/client4'
requests.post(URL, data=json.dumps(DATA), headers=HEADERS)

DATA = {
    "name":"client5",
    "number_squads": 55,
    "webhook_url": "http://127.0.0.1:5000/client5/webhook",
    "client_strategy": "random"
}
time.sleep(2)
URL = 'http://127.0.0.1:5000/client5'
requests.post(URL, data=json.dumps(DATA), headers=HEADERS)
