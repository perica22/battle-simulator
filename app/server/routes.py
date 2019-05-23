import json
from flask import request, jsonify, make_response, session, redirect, url_for

from app import app, db

from app.server.models import Army
from app.server.response import ResponseCreate
from app.server.validation import validate_army_create
from app.server.webhooks import WebhookService




@app.route('/starwars/api/join', methods=['POST'])
def join():
    webhook_service = WebhookService(topic='army.join')
    response_create = ResponseCreate()
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
    
    # triggering army.join webhook
    army_join_webhook = webhook_service.create_army_join_webhook(army)

    result = response_create.create_single_army_response(army)

    response = make_response(json.dumps(result), 200)
    response.mimetype = "application/json"
    return response


@app.route('/starwars/api/attack/<int:army_id>', methods=['PUT'])
def attack(army_id):
    rj = request.get_json()
    #import ipdb
    #ipdb.set_trace()    
    # check if army exists
    army = Army.query.filter_by(id=army_id).first()
    if army is None:
        return jsonify({"error": "army not found"}), 404

    # TODO!: here i will need to add service for attacking logic
    AttackService(rj, army).attack()

    return "this is the attack route, you can begin your attack"


@app.route('/starwars/api/leave', methods=['PUT'])
def leave():
    return "this is a leave route"
