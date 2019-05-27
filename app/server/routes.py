"""server routes"""
import json
import time

from flask import request, jsonify, make_response#, redirect, url_for

from app import APP

from .attack_service import ArmyAttackService
from .join_service import ArmyJoinService
from .utils import calculate_reload_time, validate_army_access_token
from .webhooks import WebhookService



@APP.route('/starwars/api/join', methods=['POST'])
@calculate_reload_time
def join(**kwargs):
    """
    Join army route
    """
    request_json = request.get_json()
    access_token = request.args.get('accessToken')
    join_service = ArmyJoinService(access_token, request_json)

    army, errors = join_service.create()
    if errors:
        return jsonify({"errors": errors}), 400

    join_service.trigger_webhook(army)

    result = join_service.create_join_response(army)

    response = make_response(json.dumps(result), 200)
    response.mimetype = "application/json"
    print("{} joined the game".format(army.name))
    time.sleep(kwargs['reload_time'])
    return response


@APP.route('/starwars/api/attack/<int:army_id>', methods=['PUT'])
@validate_army_access_token
@calculate_reload_time
def attack(attack_army, army_id, **kwargs):
    """
    Attack army route
    """
    attack_service = ArmyAttackService(attack_army)

    # check if army exists
    defence_army = attack_service.get_defence_army(army_id)
    if defence_army is None:
        return jsonify({"error": "army not found"}), 404

    # saving battle in the db
    battle = attack_service.create()

    # repeting the battle until success or max num of retries is reached
    for _ in range(attack_army.number_squads):
        with attack_service:
            response = attack_service.attack(battle)
            if response != 'try_again':
                # triggering webhooks for battle
                attack_service.trigger_webhooks()
                print("{} attacked successfully".format(attack_army.name))
                time.sleep(kwargs['reload_time'])
                return 'success'
                #return redirect(url_for(response))

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
