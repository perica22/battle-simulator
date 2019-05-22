import json
from flask import request, jsonify, make_response

from app import app, db

from app.models import Army
from app.response import create_single_army_response
from app.validation import validate_army_create


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


@app.route('/starwars/api/join', methods=['POST'])
def join():
    rj = request.get_json()

    # Army validation
    errors = validate_army_create(rj)
    if errors:
        return "you have an error: {}".format(errors)

    # TODO: add validation in case army.name value is not unique
    army = Army(name=rj['name'], 
        number_squads=rj['number_squads'], 
        webhook_url=rj['webhook_url'])
    db.session.add(army)
    db.session.commit()
    
    # TODO!: trigger army.join webhook and send it to all registred armys
    # with ID of the army and the number of their squads.

    # TODO!: create func for creating obj response or do a schema 
    result = create_single_army_response(army)

    response = make_response(json.dumps(result), 200)
    response.mimetype = "application/json"
    return response


@app.route('/starwars/api/attack/<int:army_id>', methods=['PUT'])
def attack(army_id):
    rj = request.get_json()

    # check if army exists
    army = Army.query.filter_by(id=army_id).first()
    if army is None:
        return jsonify({"error": "army not found"}), 404

    # TODO!: here i will need to add service for attacking logic

    return "this is the attack route, you can begin your attack"


@app.route('/starwars/api/leave', methods=['PUT'])
def leave():
    return "this is a leave route"
