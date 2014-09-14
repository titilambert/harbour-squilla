from flask.ext.restful import Resource

from squilla import api

class Networks(Resource):
    def get(self):
        data = [{"name": "eth0", "ip": "192.168.2.1"}]
        return {'networks': data}

api.add_resource(Networks, '/info/networks')
