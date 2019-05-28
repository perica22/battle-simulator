import requests
import json
import time

"""
CHECK THE WHILE LOOP IN CLINETS SECTION 
PROB THE REASON IT IS NOT WORKING 
"""

headers = {"Content-Type": "application/json"}

url ='http://127.0.0.1:5000/client1'
response = requests.post(url, data=json.dumps({}), headers=headers)

time.sleep(3)
url ='http://127.0.0.1:5000/client2'
response = requests.post(url, data=json.dumps({}), headers=headers)

time.sleep(3)
url ='http://127.0.0.1:5000/client3'
response = requests.post(url, data=json.dumps({}), headers=headers)

time.sleep(2)
url ='http://127.0.0.1:5000/client4'
response = requests.post(url, data=json.dumps({}), headers=headers)

url ='http://127.0.0.1:5000/client5'
response = requests.post(url, data=json.dumps({}), headers=headers)
