"""Handling army join """
from app import DB

from .models import Army
from .webhooks import WebhookService
from .response import ResponseCreate
from .utils import Indenter


class ArmyJoinService:
    """
    Handling army join
    Args:
        access_token: passed in case army is rejoining else None
        payload: request body on /join route
    """
    def __init__(self, access_token=None, payload=None):
        self.webhook_service = WebhookService()
        self.create_response = ResponseCreate()
        self.access_token = access_token
        self.payload = payload

    def create(self):
        """
        Creates the army and calling method for triggering army_join webhooks
        Returns:
            army instance once it is successfuly created
        """
        if self.access_token:
            army = Army.query.filter_by(
                access_token=self.access_token).first()
            army.join_type_update()
        else:
            with Indenter(-1) as indent:
                indent.print("{} joined the game".format(self.payload['name'].upper()))
        
            army = Army(name=self.payload['name'],
                        number_squads=self.payload['number_squads'],
                        webhook_url=self.payload['webhook_url'])
            DB.session.add(army)
            DB.session.commit()

            self._trigger_webhook(army)

        return army

    def _trigger_webhook(self, army):
        """
        Triggering webhook with joined army to all previously joined armies
        Triggering webhook of all previously joined armies to just joined one
        Args:
            army: instance of joined army
        """
        self.webhook_service.create_army_join_webhook(army)
        self.webhook_service.create_webhook_with_already_joined_armies(army)

    def create_join_response(self, army):
        """
        Creating join response
        """
        response = self.create_response.create_single_army_response(army)
        return response

    def validate_army_create(self):
        """
        Validating reuqest body
        Returns:
            errors list in case request body not valid
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
