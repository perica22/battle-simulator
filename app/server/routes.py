"""server routes"""
import json
import time

from flask import request, jsonify, make_response, redirect, url_for

from app import APP
from app import DB

from app.server.models import Army
from app.server.response import ResponseCreate
from app.server.validation import validate_army_create
from app.server.webhooks import WebhookService
from app.server.attack_service import AttackService
from app.server.utils import calculate_reload_time, validate_army_access_token



@APP.route('/starwars/api/join', methods=['POST'])
@calculate_reload_time
def join(**kwargs):
    """
    Join army route
    """
    webhook_service = WebhookService()
    response_create = ResponseCreate()
    request_json = request.get_json()

    # Army validation
    errors = validate_army_create(request_json)
    if errors:
        return "you have an error: {}".format(errors)

    # TODO: add validation in case army.name value is not unique
    # and possibl yremove session
    army = Army(name=request_json['name'],
                number_squads=request_json['number_squads'],
                webhook_url=request_json['webhook_url'])
    DB.session.add(army)
    DB.session.commit()

    # triggering army.join webhook
    webhook_service.create_army_join_webhook(army)

    result = response_create.create_single_army_response(army)

    response = make_response(json.dumps(result), 200)
    response.mimetype = "application/json"

    time.sleep(kwargs['reload_time'])
    return response


@APP.route('/starwars/api/attack/<int:army_id>', methods=['PUT'])
@validate_army_access_token
@calculate_reload_time
def attack(attack_army, army_id, **kwargs):
    """
    Attack army route
    """
    # check if army exists
    defence_army = Army.query.filter_by(id=army_id).first()
    if defence_army is None:
        return jsonify({"error": "army not found"}), 404

    attack_service = AttackService(attack_army, defence_army)
    # saving battle in the db
    battle = attack_service.create()

    # repeting the battle until success or max num of retries is reached
    for _ in range(attack_army.number_squads):
        with attack_service:
            response = attack_service.attack(battle)
            if response != 'try_again':
                time.sleep(kwargs['reload_time'])
                return redirect(url_for(response))

    return "this is the attack route, you can begin your attack"


@APP.route('/starwars/api/leave', methods=['POST'])
@validate_army_access_token
@calculate_reload_time
def leave(army, **kwargs):
    """
    Leave army route
    """
    webhook_service = WebhookService()

    if army.status == 'left':
        return jsonify({"error": "you already left the game"}), 200

    army.leave(leave_type='left')

    # trigger army.leave webhook
    webhook_service.create_army_leave_webhook(army, leave_type='left')

    time.sleep(kwargs['reload_time'])

    return jsonify({"success": "you have left the game"}), 200
