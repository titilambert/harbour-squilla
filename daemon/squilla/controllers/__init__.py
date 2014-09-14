from flask import send_file, make_response, abort, Blueprint, render_template

from squilla import app

from squilla.controllers import home
from squilla.controllers import echo
from squilla.controllers import menus
from squilla.controllers import modules

blueprint = Blueprint('core',
                      __name__,
                      static_url_path='/static/core',
                      static_folder='../static',
                      template_folder='templates',
#                      url_prefix='/core'
                     )
app.register_blueprint(blueprint)

# set menus
menus = {'name': 'Squilla',
         'submenus': [{'name': 'Echo',
                       'url': '/#/core/echo',
                      },
                      {'name': 'Modules',
                       'url': '/#/core/modules',
                      }
                     ]
        }

app.menus.append(menus)

