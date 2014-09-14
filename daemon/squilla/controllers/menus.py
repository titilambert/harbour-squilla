from squilla.libs import Resource

from squilla import api, app


class Menus(Resource):
    def get(self):
        return {'menus': app.menus}

api.add_resource(Menus, '/menus')
