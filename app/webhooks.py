import requests
from app.models import Army
from app.response import create_single_army_join_webhook

class WebhookService():

    def create_army_join_webhook(self, payload):
        headers = {"Content-Type": "application/json",
                   "Webhook-Topic": 'army.join'}

        armys = Army.query.filter_by(status='alive').all()

        webhook_payload = create_single_army_join_webhook(payload)

        webhook_urls = [army.webhook_url for army in armys]
        
        for url in webhook_urls:
            pass
            '''
            response = requests.post(url, data=webhook_payload, headers=headers)
            if response.status_code == 200:
                continue
            '''

    #def create_army_leave_webhook
    #def create_army_update_webhook