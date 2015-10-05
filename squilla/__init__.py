# -*- coding: utf-8 -*-

"""
    Squilla
    ~~~~~~
    :copyright: (c) 2015 by Thibault Cohen
    :license: GPLv3, see LICENSE for more details.
"""

import argparse
from wsgiref import simple_server

#from squilla.daemon import squilla_api
from daemon import squilla_api

def main():
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Listen port",
                        default=8000,
                        type=int)
    args = parser.parse_args()
    # Run server 
    httpd = simple_server.make_server('127.0.0.1', args.port, squilla_api)
    httpd.serve_forever()


if __name__ == '__main__':
    main()


__import__('pkg_resources').declare_namespace(__name__)
