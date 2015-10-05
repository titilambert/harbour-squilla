# -*- coding: utf-8 -*-

"""
    Daemon
    ~~~~~~
    :copyright: (c) 2015 by Thibault Cohen
    :license: GPLv3, see LICENSE for more details.
"""

# Let's get this party started
import falcon

# falcon.API instances are callable WSGI apps
squilla_api = falcon.API()
