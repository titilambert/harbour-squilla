import os
import glob

from flask import Blueprint

from flask.ext import restful

from squilla.libs.authentication import api_authenticate


from squilla import app


class Resource(restful.Resource):
    method_decorators = [api_authenticate]


def declare_module(module_name):
    # Import controllers
    controllers_path = os.path.join(os.path.dirname(__file__),
                                    "..",
                                    "modules",
                                    module_name,
                                    "controllers",
                                    "*.py")
    for element in glob.glob(controllers_path):
        if not os.path.isfile(element):
            continue

        _, file_name = os.path.split(element)
        if file_name == "__init__.py":
            controller_name = ".".join(("squilla.modules",
                                        module_name,
                                        "controllers"))
        else:
            controller_name, _ = os.path.splitext(file_name)
            controller_name = ".".join(("squilla.modules",
                                        module_name,
                                        "controllers",
                                        controller_name))
        try:
            __import__(controller_name)
        except Exception as exp:
            print(exp)


    blueprint = Blueprint(module_name,
                          ".".join(("squilla.modules", module_name)),
                          static_url_path='/static/info',
                          static_folder='static',
                          template_folder='templates',
                         )
    app.register_blueprint(blueprint)

def register_menu(menu):
    app.menus.append(menu)

