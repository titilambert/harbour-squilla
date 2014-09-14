from squilla.libs import Resource

from squilla import api


class Echo(Resource):
    def get(self, text):
        return {'echo': str(text)}

api.add_resource(Echo, '/echo/<string:text>')
