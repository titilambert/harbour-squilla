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


from squilla.lib.logger import logger

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



def read_configuration():
    """ Read configuration """
    try:
        CONFIG.read(CONFIG_FILE)
    except Exception as exp:
        logger.debug("Config error: " + str(exp))
        return False
    return True


def write_configuration():
    with open(CONFIG_FILE, 'w') as config_f:
        CONFIG.write(config_f)


def get_authentication():
    read_configuration()
    ret = {}

    if 'core' not in CONFIG:
        return ret

    ret['username'] = CONFIG['core'].get('username', '')
    ret['password'] = CONFIG['core'].get('password', '')
    logger.debug("Squilla username: %s" % ret['username'])
    logger.debug("Squilla password: %s" % ret['password'])

    return ret


def set_authentication(key, value):
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
