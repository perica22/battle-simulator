"""Handling army join """
from app import DB

from .models import Army
from .webhooks import WebhookService
from .response import ResponseCreate



class ArmyJoinService:
    """
    Handling army join
    """
    def __init__(self, access_token=None, payload=None):
        self.webhook_service = WebhookService()
        self.create_response = ResponseCreate()
        self.access_token = access_token
        self.payload = payload

    def create(self):
        """Creating or rejoyning armys"""
        if self.access_token:
            army = Army.query.filter_by(
                access_token=self.access_token).first()
            army.join_type_update()
        else:
            errors = self._validate_army_create()
            if errors:
                return None, errors
            army = Army(name=self.payload['name'],
                        number_squads=self.payload['number_squads'],
                        webhook_url=self.payload['webhook_url'])
            DB.session.add(army)
            DB.session.commit()

        return army, None

    def trigger_webhook(self, army):
        """Triggering webhook"""
        self.webhook_service.create_army_join_webhook(army)

    def create_join_response(self, army):
        """Creating join response"""
        response = self.create_response.create_single_army_response(army)
        return response

    def _validate_army_create(self):
        """
        Checking required params
        """
        errors = []
        if 'name' not in self.payload:
            errors.append('name is required field')

        if 'number_squads' not in self.payload:
            errors.append('number_squads is required field')
        else:
            if self.payload['number_squads'] > 100 or self.payload['number_squads'] < 10:
                errors.append('number_squads must be between 10 and 100')

        if 'webhook_url' not in self.payload:
            errors.append('webhook_url is required field')

        return errors
