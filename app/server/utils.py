"""
help functions for server
"""
import math

from functools import wraps

from flask import request, jsonify

from .models import Army



def calculate_reload_time(function):
    """
    Decorator calculating server reload time
    Args:
        number_squads: used to calcualte response delay of server
    Returns:
        reload_time: sleep time of server before returning response
    Exception:
        IndexError: in case decorator is used on routes other then join
        TypeError: in case on join route number_squads is not in body 
    """
    @wraps(function)
    def decorated(*args):
        try:
            number_squads = args[0].number_squads
        except IndexError:
            try:
                number_squads = request.get_json()['number_squads']
                kwargs['reload_time'] = math.floor(number_squads / 10)
            except TypeError:
                pass

        return function(reload_time)
    return decorated

def validate_army_access_token(function):
    """
    Decorator checking access token
    Args:
        access_token: value to be validated by querying DB
    Returns:
        army instance
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

class Indenter:
    """
    Indenter for printing console logs
    Args:
        level: number of indents before print
    """
    def __init__(self, level):
        self.level = level
    def __enter__(self):
        self.level += 1
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1
    def print(self, text):
        """printing intented messages to console"""
        print('     ' * self.level + text)
