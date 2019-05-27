"""
Creating API responses
"""
from collections import OrderedDict


class ResponseCreate:
    """
    Creating API responses
    """
    def __init__(self):
        self.obj = {}

    def _wrap_response(self):
        """wrapping response into ARMY key"""
        result_with_wrapper = {}
        result_with_wrapper['army'] = self.obj
        return result_with_wrapper

    def create_single_army_response(self, data):
        """Creating army responses"""
        self.obj['id'] = data.id
        self.obj['name'] = data.name
        self.obj['squadsCount'] = data.number_squads
        self.obj['webhookUrl'] = data.webhook_url
        self.obj['accessToken'] = data.access_token

        result = self._wrap_response()

        return OrderedDict(result)

    def create_army_join_webhook_response(self, data):
        """Creating army.join webhook response"""
        self.obj['armyId'] = data.id
        self.obj['squadsCount'] = data.number_squads
        self.obj['TypeOfJoin'] = data.join_type

        result = self._wrap_response()

        return OrderedDict(result)

    def create_army_update_webhook_response(self, data):
        """Creating army.update webhook response"""
        self.obj['armyId'] = data.id
        self.obj['squadsCount'] = data.number_squads
        self.obj['rankRate'] = data.rankRate

        result = self._wrap_response()

        return OrderedDict(result)

    def create_army_leave_webhook_response(self, data, leave_type):
        """Creating army.leave webhook response"""
        self.obj['armyId'] = data.id
        self.obj['TypeOfLeave'] = leave_type

        result = self._wrap_response()

        return OrderedDict(result)
