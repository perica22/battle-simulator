"""INITIAL SCRIPT"""
import json
import time
import requests
from threading import Thread



HEADERS = {"Content-Type": "application/json"}

# data used to create clients
list_data = [
    {
        "url":"http://127.0.0.1:5000/client1",
        "name":"client1",
        "number_squads": 85,
        "webhook_url": "http://127.0.0.1:5000/client1/webhook",
        "client_strategy": "random"
    },
    {
        "url":"http://127.0.0.1:5000/client2",
        "name":"client2",
        "number_squads": 76,
        "webhook_url": "http://127.0.0.1:5000/client2/webhook",
        "client_strategy": "max"
    },
    {
        "url":"http://127.0.0.1:5000/client3",
        "name":"client3",
        "number_squads": 65,
        "webhook_url": "http://127.0.0.1:5000/client3/webhook",
        "client_strategy": "random"
    },
    {
        "url":"http://127.0.0.1:5000/client4",
        "name":"client4",
        "number_squads": 35,
        "webhook_url": "http://127.0.0.1:5000/client4/webhook",
        "client_strategy": "min"
    },
    {
        "url":"http://127.0.0.1:5000/client5",
        "name":"client5",
        "number_squads": 55,
        "webhook_url": "http://127.0.0.1:5000/client5/webhook",
        "client_strategy": "random"
    },
    {
        "url":"http://127.0.0.1:5000/client6",
        "name":"client6",
        "number_squads": 55,
        "webhook_url": "http://127.0.0.1:5000/client6/webhook",
        "client_strategy": "random"
    },
    {
        "url":"http://127.0.0.1:5000/client7",
        "name":"client7",
        "number_squads": 55,
        "webhook_url": "http://127.0.0.1:5000/client7/webhook",
        "client_strategy": "random"
    },
    {
        "url":"http://127.0.0.1:5000/client8",
        "name":"client8",
        "number_squads": 55,
        "webhook_url": "http://127.0.0.1:5000/client8/webhook",
        "client_strategy": "random"
    },
    {
        "url":"http://127.0.0.1:5000/client9",
        "name":"client9",
        "number_squads": 55,
        "webhook_url": "http://127.0.0.1:5000/client9/webhook",
        "client_strategy": "random"
    }
]

def make_request(DATA):
    '''making request'''
    requests.post(DATA['url'], data=json.dumps(DATA), headers=HEADERS)

# using threads to join all clients
for data in list_data:
    time.sleep(10) # time sleep to create delay between joins
    thread = Thread(target=make_request, args=(data,))
    thread.start()

thread.join()
