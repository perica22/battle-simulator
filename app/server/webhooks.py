"""Building webhooks"""
import json
import requests

from .models import Army
from .response import ResponseCreate



class WebhookService:
    """
    Service for handling webhooks
    """
    def __init__(self):
        self.headers = {"Content-Type": "application/json",
                        "Webhook-Topic": None}
        self.response_create = ResponseCreate()

    def create_army_join_webhook(self, payload):
        """Logic for creating army.join webhook"""
        self.headers["Webhook-Topic"] = "army.join"
        armys = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_join_webhook_response(payload)

        webhook_urls = [army.webhook_url for army in armys]
        for url in webhook_urls:
            print("{}; army.join webhook sent to {}".format(webhook_payload, url))
            requests.post(
                url, data=json.dumps(webhook_payload), headers=self.headers)

    def create_army_leave_webhook(self, payload, leave_type):
        """Logic for creating army.leave webhook"""
        self.headers["Webhook-Topic"] = "army.leave"

        armys = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_leave_webhook_response(
            payload, leave_type)

        webhook_urls = [army.webhook_url for army in armys]
        for url in webhook_urls:
            print("{}; army.leave webhook sent to {}".format(webhook_payload, url))
            requests.post(
                url, data=json.dumps(webhook_payload), headers=self.headers)

    def create_army_update_webhook(self, army):
        """Logic for creating army.update webhook"""
        self.headers["Webhook-Topic"] = "army.update"

        # determining rank-rate of army
        armys = Army.query.order_by(Army.number_squads.desc()).all()
        army.rankRate = armys.index(army) + 1

        webhook_payload = self.response_create.create_army_update_webhook_response(army)

        url = army.webhook_url
        print("{}; army.update webhook sent to {}".format(webhook_payload, url))
        requests.post(
            url, data=json.dumps(webhook_payload), headers=self.headers)
