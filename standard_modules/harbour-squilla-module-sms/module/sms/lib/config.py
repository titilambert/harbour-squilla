#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    config.py
#
#    This file is part of Squilla
#
#    Copyright (C) 2014 Thibault Cohen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


import os

try:
    import configparser
    CONFIG = configparser.ConfigParser()
except Exception as exp:
    pass


from squilla.libs.config import load_setting, save_setting
from squilla.libs.logger import logger

# Squilla config folder
#CONFIG_FOLDER = os.path.join(os.environ.get('HOME'),
CONFIG_FOLDER = os.path.join('/home/nemo/',
                             ".config/harbour-squilla/")
# Squilla config file path
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.ini")

# Create config folder
if not os.path.exists(CONFIG_FOLDER):
    os.makedirs(CONFIG_FOLDER)

if not os.path.isdir(CONFIG_FOLDER):
    raise Exception("'%s' must be a folder" % CONFIG_FOLDER)





def get_interface_name():
    settings = load_setting()

    connection = settings.get('connection', 'wifi')

    if connection not in ['usb', 'wifi']:
        return 'wifi'

    return connection


def get_bridges():
    settings = load_setting()
    bridges = []
    for bridge in ['http', 'bonjour']:
        if settings.get(bridge, False) == 'True':
            bridges.append(bridge)
    return bridges


def get_favorites():
    settings = load_setting()

    if 'favorites' not in settings:
        return []

    # Get favorites
    return [f for f in settings['favorites'].items()]


def get_last_presence_auth_user():
    settings = load_setting()

    if 'auth_user' not in settings:
        return None

    auth_user = settings.get('auth_user', None)

    return auth_user



def save_last_presence_auth_user(auth_user):
    """ auth_user must be str or NoneType """
    if auth_user is not None:
        save_setting('auth_user', str(auth_user))















def is_favorite(number):
    read_configuration()

    if 'favorites' not in CONFIG:
        return False

    name = CONFIG['favorites'].get(number, False)

    if name:
        return True

    return False


def set_favorite(number, name):
    read_configuration()

    # Set empty config
    if 'favorites' not in CONFIG:
        CONFIG['favorites'] = {}

    # Append or remove favorites
    if not is_favorite(number):
        CONFIG['favorites'][number] = name
        ret = True
    else:
        CONFIG['favorites'].pop(number)
        ret = False

    # Save
    write_configuration()

    # True == favorite
    # False == not favorite
    return ret


def set_silent_mode(state):
    read_configuration()

    # Set empty general
    if 'general' not in CONFIG:
        CONFIG['general'] = {}

    if int(CONFIG['general'].get('silent_mode', 0)) == 0:
        CONFIG['general']['silent_mode'] = '1'
    else:
        CONFIG['general']['silent_mode'] = '0'

    # Save
    write_configuration()


def get_silent_mode():
    # Set empty general
    if 'general' not in CONFIG:
        return False

    return bool(int(CONFIG['general'].get('silent_mode', 0)))


def set_interface_name(connection):
    read_configuration()

    # Set empty general
    if 'general' not in CONFIG:
        CONFIG['general'] = {}

    CONFIG['general']['connection'] = connection

    # Save
    write_configuration()


def save_presence_auth_user(auth_user):
    read_configuration()

    # Set empty general
    if 'general' not in CONFIG:
        CONFIG['general'] = {}

    CONFIG['general']['auth_user'] = auth_user['name']

    # Save
    write_configuration()


def load_presence_auth_user():
    read_configuration()

    # if general doesn't exist
    if 'general' not in CONFIG:
        return None

    auth_user = CONFIG['general'].get('auth_user', None)

    return auth_user

