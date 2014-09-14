from flask import send_file, make_response, abort, Blueprint, render_template

from squilla import app
from squilla.libs.config import load_setting, save_setting

from squilla.controllers import home
from squilla.controllers import echo
from squilla.controllers import config
from squilla.controllers import menus
from squilla.controllers import modules

# Register blueprint
blueprint = Blueprint('core',
                      __name__,
                      static_url_path='/static/core',
                      static_folder='../static',
                      template_folder='templates',
                     )
app.register_blueprint(blueprint)

# Set menus
menus = {'name': 'Squilla',
         'submenus': [
                      {'name': 'Configuration',
                       'url': '/#/core/config',
                      },

                      {'name': 'Echo',
                       'url': '/#/core/echo',
                      },
                      {'name': 'Modules',
                       'url': '/#/core/modules',
                      }
                     ]
        }
app.menus.append(menus)

# Set default values
settings = load_setting()
if settings is None or 'username' not in settings:
    save_setting('username', 'jolla')
if settings is None or 'password' not in settings:
    save_setting('password', 'squilla')
