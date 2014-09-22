import re
import subprocess

from flask.ext.restful import reqparse
from flask.ext.restful import Resource

from squilla.libs.config import load_setting, save_setting
from squilla import api

parser = reqparse.RequestParser()
parser.add_argument('connection', type=str)
parser.add_argument('presence', type=str)
parser.add_argument('http', type=str)
parser.add_argument('bonjour', type=str)
parser.add_argument('autostart', type=str)
parser.add_argument('silent', type=str)
parser.add_argument('controller', type=str)

class ConfigSave(Resource):
    def post(self):
        config = parser.parse_args()
        for key, value in config.items():
            if value is None:
                value = "False"
            save_setting(key, value)
        return {"state": 'success',
                "message": 'Configuration successfully saved',
               }

class ConfigLoad(Resource):
    def get(self):
        raw_settings = load_setting()
        settings = {}
        for setting, value in raw_settings.items():
            if value == 'True':
                settings[setting] = True
            if value == 'False':
                settings[setting] = False
            else:
                settings[setting] = value
        return settings

api.add_resource(ConfigSave, '/sms/config/save')
api.add_resource(ConfigLoad, '/sms/config/load')
