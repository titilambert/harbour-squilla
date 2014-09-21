import os
import glob

from flask import send_file, make_response, abort, Blueprint, render_template

from squilla import app
from squilla.libs import declare_module, register_menu


# Register it menu
menu = {'name': 'System',
        'submenus': [{'name': 'Network',
                      'url': '/#/system/network',
                     }
                    ]
       }
register_menu(menu)

