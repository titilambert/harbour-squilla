import re
import subprocess

from flask.ext.restful import reqparse
from flask.ext.restful import Resource

from squilla.libs.config import load_setting, save_setting
from squilla import api

from ..sms import app
from ..sms.lib.config import get_last_presence_auth_user



parser = reqparse.RequestParser()
parser.add_argument('connection', type=str)
parser.add_argument('presence', type=str)
parser.add_argument('http', type=str)
parser.add_argument('bonjour', type=str)
parser.add_argument('autostart', type=str)
parser.add_argument('silent', type=str)
parser.add_argument('controller', type=str)


class PresenceUsers(Resource):
    def get(self):
        if not app.started or not 'bonjour' in app.bridges:
            return {}
        app.load_presences()
        #return [{'data': {'host': '192.168.2.11', 'port': 5298, 'raw_name': 'BBBB@absol._presence._tcp.local.', 'name': 'BBBB', 'hostname': 'absol.local.'}, 'name': 'BBBB'}, {'data': {'host': '192.168.2.11', 'port': 5299, 'raw_name': 'titilambert@absol.home.titilambert.org._presence._tcp.local.', 'name': 'titilambert', 'hostname': 'absol.local.'}, 'name': 'titilambert'}]
        return app.available_presence_users


class PresenceAuthUser(Resource):
    def get(self):
        """ Return current presence auth user """
        return {"name": get_last_presence_auth_user()}

    def post(self):
        """ Save presence auth user"""
        return {"status": "success",
                "message": "Authorized user saved successfully"
               }

api.add_resource(PresenceUsers, '/sms/bonjour/users')
api.add_resource(PresenceAuthUser, '/sms/bonjour/auth_user')
