import os
import glob

from flask import send_file, make_response, abort, Blueprint, render_template

from squilla import app
from squilla.libs import declare_module, register_menu


# Declare module
declare_module('info')
# Register it menu
menu = {'name': 'Info',
        'submenus': [{'name': 'Network',
                      'url': '/#/info/network',
                     }
                    ]
       }

register_menu(menu)

