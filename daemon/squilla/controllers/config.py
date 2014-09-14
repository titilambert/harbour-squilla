
from flask.ext.restful import reqparse

from squilla.libs import Resource
from squilla.libs.config import load_setting, save_setting

from squilla import api

parser = reqparse.RequestParser()
parser.add_argument('password', type=str)
parser.add_argument('username', type=str)

class Config(Resource):
    def get(self):
        settings = load_setting()
        settings = dict([i for i in settings.items()])
        return settings

    def post(self):
        config = parser.parse_args()
        for key, value in config.items():
            if value is not None:
                save_setting(key, value)
        return  {"state": 'success', 
                 "message": 'Configuration successfully saved',
                }

api.add_resource(Config, '/core/config')
