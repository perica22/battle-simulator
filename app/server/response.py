from collections import OrderedDict


class ResponseCreate:

    def create_single_army_response(self, data):
        obj = {}

        obj['id'] =  data.id
        obj['name'] =  data.name
        obj['number_squads'] =  data.number_squads
        obj['webhook_url'] =  data.webhook_url
        obj['access_token'] =  data.access_token

        result_with_wrapper = {}
        result_with_wrapper['army'] = obj

        return OrderedDict(result_with_wrapper)

    def create_army_join_webhook_response(self, data):
        obj = {}

        obj['id'] = data.id
        obj['number_squads'] = data.number_squads
        obj['join_type'] = data.join_type

        result_with_wrapper = {}
        result_with_wrapper['army'] = obj

        return OrderedDict(result_with_wrapper)
