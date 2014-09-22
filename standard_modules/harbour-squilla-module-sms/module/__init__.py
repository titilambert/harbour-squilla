import os
import sys
import glob

from flask import send_file, make_response, abort, Blueprint, render_template

from squilla import app
from squilla.libs import declare_module, register_menu


embedded_libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  './embedded_libs/')
sys.path.append(embedded_libs_path)


# Register it menu
menu = {'name': 'SMS',
        'submenus': [
                     {'name': 'Home',
                      'url': '/#/sms/home',
                     },
                     {'name': 'Config',
                      'url': '/#/sms/config',
                     },
                    ]
       }
register_menu(menu)

