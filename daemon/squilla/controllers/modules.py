from squilla.libs import Resource

from squilla import api, app


class Modules(Resource):
    def get(self):
        return {'modules': app.module_list}

api.add_resource(Modules, '/core/modules')
