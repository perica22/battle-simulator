import requests
import json
from app.server.models import Army
from app.server.response import create_single_army_join_webhook

class WebhookService():

    def create_army_join_webhook(self, payload):
        headers = {"Content-Type": "application/json",
                   "Webhook-Topic": 'army.join'}

        armys = Army.query.filter_by(status='alive').all()
        url =str(payload.webhook_url)
        webhook_payload = create_single_army_join_webhook(payload)
        #response = requests.post(url, data=json.dumps(webhook_payload), headers=headers)
        webhook_urls = [army.webhook_url for army in armys]
        
        for url in webhook_urls:
            pass
           
            response = requests.post(url, data=json.dumps(webhook_payload), headers=headers)
            if response.status_code == 200:
                continue

    #def create_army_leave_webhook
    #def create_army_update_webhook