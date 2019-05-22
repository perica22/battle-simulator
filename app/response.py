from collections import OrderedDict


def create_single_army_response(data):
    obj = {}

    obj['id'] =  data.id
    obj['name'] =  data.name
    obj['number_squads'] =  data.number_squads
    obj['webhook_url'] =  data.webhook_url

    result_with_wrapper = {}
    result_with_wrapper['army'] = obj

    return OrderedDict(result_with_wrapper)
