from flask import request
from app import app


def validate_army_create(payload):
    errors = []
    if 'name' not in payload:
        errors.append('name is required field')
    if 'number_squads' not in payload:
        errors.append('number_squads is required field')
    if 'webhook_url' not in payload:
        errors.append('webhook_url is required field')

    return errors


@app.route('/starwars/api/join', methods=['POST'])
def join():
    rj = request.get_json()

    # Army validation
    errors = validate_army_create(rj)

    if errors:
        return "you have an error: {}".format(errors)

    return "this is a join route with following data: {}, {}, {}".format(rj['name'], rj['number_squads'], rj['webhook_url'])

@app.route('/starwars/api/attack/<int:army_id>')
def attack(army_id):
    return "this is the attack route"

@app.route('/starwars/api/leave')
def leave():
    return "this is a leave route"
