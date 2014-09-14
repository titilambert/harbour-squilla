from functools import wraps
from flask.ext import restful
from flask import request, Response

from squilla.libs.config import load_setting

# auth for /

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    saved_username = load_setting(None, 'username', 'jolla')
    saved_password = load_setting(None, 'password', 'squilla')
    return username == saved_username and password == saved_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


### Auth for API

def api_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            restful.abort(401)
        return func(*args, **kwargs)
    return wrapper
