"""
Creating API responses
"""
from collections import OrderedDict


class ResponseCreate:
    """
    Creating API responses
    """
    def __init__(self):
        self.key = 'army'

    def _wrap_response(self, obj):
        """wrapping response into ARMY key"""
        result_with_wrapper = {}
        result_with_wrapper[self.key] = obj
        return result_with_wrapper

    def create_single_army_response(self, data):
        """Creating army responses"""
        obj = {}
        obj['id'] = data.id
        obj['name'] = data.name
        obj['squadsCount'] = data.number_squads
        obj['webhookUrl'] = data.webhook_url
        obj['accessToken'] = data.access_token

        result = self._wrap_response(obj)

        return OrderedDict(result)

    def create_army_join_webhook_response(self, data):
        """Creating army.join webhook response"""
        obj = {}
        obj['armyId'] = data.id
        obj['squadsCount'] = data.number_squads
        obj['TypeOfJoin'] = data.join_type

        result = self._wrap_response(obj)

        return OrderedDict(result)

    def create_army_update_webhook_response(self, data):
        """Creating army.update webhook response"""
        obj = {}
        obj['armyId'] = data.id
        obj['squadsCount'] = data.number_squads
        obj['rankRate'] = data.rankRate

        result = self._wrap_response(obj)

        return OrderedDict(result)

    def create_army_leave_webhook_response(self, data, leave_type):
        """Creating army.leave webhook response"""
        obj = {}
        obj['armyId'] = data.id
        obj['TypeOfLeave'] = leave_type

        result = self._wrap_response(obj)

        return OrderedDict(result)

    def webhook_response_with_already_joined_armies(self, armies):
        """Creating list of armies for army.join webhook response"""
        obj = []

        response = {}
        for army in armies:
            response['armyId'] = army.id
            response['squadsCount'] = army.number_squads
            response['TypeOfJoin'] = army.join_type
            obj.append(response)

        self.key = 'armies'
        result = self._wrap_response(obj)

        return OrderedDict(result)
