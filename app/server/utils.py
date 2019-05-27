"""
help functions for server
"""
import math
from functools import wraps

from flask import request, jsonify

from .models import Army #token - for showing DB relations



def calculate_reload_time(function):
    """
    This is the decorator calculating server reload time
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            number_squads = args[0].number_squads
        except IndexError:
            number_squads = request.get_json()['number_squads']
        kwargs['reload_time'] = math.floor(number_squads / 10 *5)
        return function(*args, **kwargs)
    return decorated

def validate_army_access_token(function):
    """
    This is the decorator checking access token.
    """
    @wraps(function)
    def decorated(**kwargs):
        access_token = request.args.get('accessToken')
        army = Army.query.filter_by(
            access_token=access_token).first()
        if not army:
            return jsonify({"error": "invalid access_token"}), 404
        return function(army, **kwargs)
    return decorated
