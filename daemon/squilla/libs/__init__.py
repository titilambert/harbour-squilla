import os
import glob

from flask import Blueprint

from flask.ext import restful

from squilla.libs.authentication import api_authenticate


from squilla import app


class Resource(restful.Resource):
    method_decorators = [api_authenticate]


def declare_module(module_name):
    # Get controllers path
    controllers_path = os.path.join(os.path.dirname(__file__),
                                    "..",
                                    "modules",
                                    module_name,
                                    "controllers",
                                    "*.py")
    # Import controllers
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
        # Import controller
        __import__(controller_name)
    # Register blueprint
    blueprint = Blueprint(module_name,
                          ".".join(("squilla.modules", module_name)),
                          static_url_path='/static/' + module_name,
                          static_folder='static',
                          template_folder='templates',
                         )
    app.register_blueprint(blueprint)

def register_menu(menu):
    app.menus.append(menu)

