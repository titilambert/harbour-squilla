import re
import subprocess

from flask.ext.restful import reqparse
from flask.ext.restful import Resource

from squilla.libs.config import load_setting, save_setting
from squilla import api

from ..sms import app


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
        if not app.started or not 'bonjour' in self.bridges::
            return {}
        #import pdb;pdb.set_trace()
        return settings

api.add_resource(PresenceUsers, '/sms/bonjour/users/get')
