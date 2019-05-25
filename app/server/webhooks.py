import requests
import json

from app.server.models import Army
from app.server.response import ResponseCreate



class WebhookService:

    def __init__(self, topic):
        self.topic = topic
        self.headers = {"Content-Type": "application/json",
                        "Webhook-Topic": self.topic}
        self.response_create = ResponseCreate()

    def create_army_join_webhook(self, payload):
        armys = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_join_webhook_response(payload)

        webhook_urls = [army.webhook_url for army in armys]
        for url in webhook_urls:
            response = requests.post(
                url, data=json.dumps(webhook_payload), headers=self.headers)
            if response.status_code == 200:
                continue

    def create_army_leave_webhook(self, payload):
        pass

    def create_army_update_dead_webhook(self, payload):
        url = payload.webhook_url
        webhook_payload = self.response_create.create_army_update_webhook_response(payload)

        response = requests.post(
            url, data=json.dumps(webhook_payload), headers=self.headers)

    def create_army_update_alive_webhook(self, payload):
        armys = Army.query.filter(Army.status == 'alive').all()
        webhook_payload = self.response_create.create_army_update_webhook_response(payload)

        webhook_urls = [army.webhook_url for army in armys]
        for url in webhook_urls:
            response = requests.post(
                url, data=json.dumps(webhook_payload), headers=self.headers)
            if response.status_code == 200:
                continue
