#!/usr/bin/python3

# -*- coding: utf-8 -*-
import re
import sys
import os

# Add embedded_libs folder
embedded_libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  'embedded_libs')
sys.path.append(embedded_libs_path)


#TODO Permit to change port
PORT = str(5000)
argv = ['-w', '1', '-D', '-b', '0.0.0.0:' + PORT, 'squilla:app']

from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    argv_0 = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv = [argv_0] + argv
    print("OKKKKKK")
    sys.exit(run())
