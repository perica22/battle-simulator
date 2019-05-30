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
        """
        Logic for creating army.join webhook
        Sending the data of army that just joined to all joined armies
        """
        self.headers["Webhook-Topic"] = "army.join"
        armies = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_join_webhook_response(payload)

        self._send_requests(armies, webhook_payload)

    def create_army_leave_webhook(self, payload, leave_type):
        """Logic for creating army.leave webhook"""
        self.headers["Webhook-Topic"] = "army.leave"

        armies = Army.query.filter(Army.status == 'alive', Army.id != payload.id).all()
        webhook_payload = self.response_create.create_army_leave_webhook_response(
            payload, leave_type)

        self._send_requests(armies, webhook_payload)

    def create_army_update_webhook(self, army):
        """Logic for creating army.update webhook"""
        self.headers["Webhook-Topic"] = "army.update"

        # determining rank-rate of army
        armies = Army.query.order_by(Army.number_squads.desc()).all()
        army.rankRate = armies.index(army) + 1

        webhook_payload = self.response_create.create_army_update_webhook_response(army)

        self._send_requests(armies, webhook_payload)

    def create_webhook_with_already_joined_armies(self, army):
        """
        Logic for creating army.join webhook
        Sending the data of all joined armies to army that just joined
        """
        self.headers["Webhook-Topic"] = "army.join"
        armies = Army.query.filter(Army.status == 'alive', Army.id != army.id).all()
        webhook_payload = self.response_create.webhook_response_with_already_joined_armies(armies)

        self._send_request(army.webhook_url, webhook_payload)

    def _send_requests(self, armies, payload):
        '''
        Making requests for sending webhooks
        '''
        for army in armies[::-1]:
            response = requests.post(
                army.webhook_url, data=json.dumps(payload), headers=self.headers)
            if response.status_code != 200:
                print("OPSSS")

    def _send_request(self, url, payload):
        '''
        Making request for sending webhook
        '''
        response = requests.post(
            url, data=json.dumps(payload), headers=self.headers)
        if response.status_code != 200:
            print("OPSSS")
