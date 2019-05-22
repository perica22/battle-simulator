
def validate_army_create(payload):
    errors = []
    if 'name' not in payload:
        errors.append('name is required field')

    if 'number_squads' not in payload:
        errors.append('number_squads is required field')
    else:
        if payload['number_squads'] > 100 or payload['number_squads'] < 10:
            errors.append('number_squads must be between 10 and 100')

    if 'webhook_url' not in payload:
        errors.append('webhook_url is required field')

    return errors
