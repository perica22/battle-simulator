"""INITIAL SCRIPT"""
import json
import time
import requests



HEADERS = {"Content-Type": "application/json"}
try:
    URL = 'http://127.0.0.1:5000/client2'
    requests.post(URL, data=json.dumps({}), headers=HEADERS)

    time.sleep(3)
    URL = 'http://127.0.0.1:5000/client3'
    requests.post(URL, data=json.dumps({}), headers=HEADERS)

    time.sleep(3)
    URL = 'http://127.0.0.1:5000/client1'
    requests.post(URL, data=json.dumps({}), headers=HEADERS)

    time.sleep(5)
    URL = 'http://127.0.0.1:5000/client4'
    requests.post(URL, data=json.dumps({}), headers=HEADERS)

    time.sleep(8)
    URL = 'http://127.0.0.1:5000/client5'
    requests.post(URL, data=json.dumps({}), headers=HEADERS)
except Exception as exception:
    print('-----------'+str(exception)+'------------')
