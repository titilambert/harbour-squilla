import glob
import os

from flask import Flask
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Init menus
app.menus = []

# Import core
from squilla import controllers

# Import modules
app.module_list = {"available": [],
                   "loaded": []
                  }
for element in glob.glob("squilla/modules/*"):
    if not os.path.isdir(element):
        continue
    splitted_path = element.split("/")
    if splitted_path[-1] == "__pycache__":
        continue
    module_name = ".".join(splitted_path)
    app.module_list['available'].append(splitted_path[-1])
    try:
        __import__(module_name)
        app.module_list['loaded'].append(splitted_path[-1])
    except Exception as exp:
        print(exp)


if __name__ == '__main__':
    app.run()

