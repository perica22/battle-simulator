"""INITIAL SCRIPT"""
import requests
import json
import time



headers = {"Content-Type": "application/json"}
try:
    url ='http://127.0.0.1:5000/client1'
    response = requests.post(url, data=json.dumps({}), headers=headers)

    time.sleep(3)
    url ='http://127.0.0.1:5000/client2'
    response = requests.post(url, data=json.dumps({}), headers=headers)

    time.sleep(3)
    url ='http://127.0.0.1:5000/client3'
    response = requests.post(url, data=json.dumps({}), headers=headers)

    time.sleep(5)
    url ='http://127.0.0.1:5000/client4'
    response = requests.post(url, data=json.dumps({}), headers=headers)
    time.sleep(8)
    url ='http://127.0.0.1:5000/client5'
    response = requests.post(url, data=json.dumps({}), headers=headers)
except Exception as e:
    print('-----------'+str(e)+'------------')