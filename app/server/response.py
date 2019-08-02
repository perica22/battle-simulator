"""
Creating API responses
"""


class ResponseCreate:
    """
    Creating API responses
    """
    def __init__(self):
        self.key = 'army'

    def _wrap_response(self, obj):
        """
        Wrapping response into self.key value
        """
        result_with_wrapper = {}
        result_with_wrapper[self.key] = obj
        return result_with_wrapper

    def create_single_army_response(self, data):
        """
        Creating army responses
        Args: 
            data: instance from which response is created
        Returns:
            army join response data
        """
        obj = {}
        obj['id'] = data.id
        obj['name'] = data.name
        obj['squadsCount'] = data.number_squads
        obj['webhookUrl'] = data.webhook_url
        obj['accessToken'] = data.access_token

        result = self._wrap_response(obj)

        return result

    def create_army_join_webhook_response(self, data):
        """
        Creating army.join webhook response
        Args: 
            data: instance from which response is created
        Returns:
            army join webhook response data
        """
        obj = {}
        obj['armyId'] = data.id
        obj['squadsCount'] = data.number_squads
        obj['TypeOfJoin'] = data.join_type
    
        result = self._wrap_response(obj)

        return result

    def create_army_update_webhook_response(self, data):
        """
        Creating army.update webhook response
        Args: 
            data: instance from which response is created
        Returns:
            army update webhook response data
        """
        obj = {}
        obj['armyId'] = data.id
        obj['squadsCount'] = data.number_squads
        obj['rankRate'] = data.rankRate

        result = self._wrap_response(obj)

        return result

    def create_army_leave_webhook_response(self, data, leave_type):
        """
        Creating army.leave webhook response
        Args: 
            data: instance from which response is created
            leave_type: died or left
        Returns:
            army leave webhook response data
        """
        obj = {}
        obj['armyId'] = data.id
        obj['TypeOfLeave'] = leave_type

        result = self._wrap_response(obj)

        return result

    def webhook_response_with_already_joined_armies(self, armies):
        """
        Creating list of armies for army.join webhook response
        Args: 
            armies: list of armies that are already in game
        """
        def to_json(data):
            return {
                'armyId': data.id,
                'squadsCount': data.number_squads,
                'TypeOfJoin': data.join_type,
            }
        result = {'armies': list(map(lambda data: to_json(data), armies))}

        return OrderedDict(result)
