"""
Creating API responses
"""
from collections import OrderedDict


class ResponseCreate:
    """Creating API responses"""
    def __init__(self):
        self.obj = {}

    def wrap_response(self):
        result_with_wrapper = {}
        result_with_wrapper['army'] = self.obj
        return result_with_wrapper

    def create_single_army_response(self, data):
        self.obj['id'] = data.id
        self.obj['name'] = data.name
        self.obj['number_squads'] = data.number_squads
        self.obj['webhook_url'] = data.webhook_url
        self.obj['access_token'] = data.access_token

        result = self.wrap_response()

        return OrderedDict(result)

    def create_army_join_webhook_response(self, data):
        self.obj['id'] = data.id
        self.obj['number_squads'] = data.number_squads
        self.obj['join_type'] = data.join_type

        result = self.wrap_response()

        return OrderedDict(result)

    def create_army_update_webhook_response(self, data):
        self.obj['id'] = data.id
        self.obj['squadsCount'] = data.number_squads
        # TODO rank-rate
        #obj['rankRate'] =

        result = self.wrap_response()

        return OrderedDict(result)

    def create_army_leave_webhook_response(self, data, leave_type):
        self.obj['id'] = data.id
        self.obj['typeOfLeave'] = leave_type

        result = self.wrap_response()

        return OrderedDict(result)
