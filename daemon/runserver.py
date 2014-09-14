#!/usr/bin/python3.4

import os, sys

# Add embedded_libs folder
embedded_libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'embedded_libs')
sys.path.append(embedded_libs_path)

# Import squilla
from squilla import app

def runserver():
    """ Run server """
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    runserver()

