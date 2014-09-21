import glob
import os
import sys

from flask import Flask
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Init menus
app.menus = []

# Import core
from squilla import controllers

# Import modules
## Get declare_module function
from squilla.libs import declare_module
## Add modules dir to path
modules_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'modules/')
sys.path.append(modules_path)
## Prepare module lists
app.module_list = {"available": [],
                   "loaded": []
                  }
## Browse avalaible modules
for element in glob.glob(modules_path + "/*"):
    if not os.path.isdir(element):
        continue
    splitted_path = element.split("/")
    if splitted_path[-1] == "__pycache__":
        continue
    # Get module name
    module_name = splitted_path[-1]
    # Append it to avalaible module list
    app.module_list['available'].append(module_name)
    # Declare module 
    try:
        declare_module(module_name)
        # Append it to loaded module list
        app.module_list['loaded'].append(module_name)
    except Exception as exp:
        print(exp)


if __name__ == '__main__':
    app.run()

