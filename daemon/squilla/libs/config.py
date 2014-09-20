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
import inspect

try:
    import configparser
    CONFIG = configparser.ConfigParser()
except Exception as exp:
    print(exp)
    pass


#from squilla.lib.logger import logger

# Squilla config folder
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


def save_setting(setting, value, section=None):
    read_configuration()
    # Detect module_name
    caller_file_name = inspect.stack()[1][1]
    if caller_file_name.find("modules") == -1:
        module_name = "core"
    else:
        print("MODULE")

    # Set empty module_name
    if module_name not in CONFIG:
        CONFIG[module_name] = {}

    # Set value
    CONFIG[module_name][setting] = value

    # write
    write_configuration()


def load_setting(section=None, setting=None, default=None):
    # Detect module_name
    caller_file_name = inspect.stack()[1][1]
    if caller_file_name.find("modules") == -1:
        module_name = "core"
    else:
        print("MODULE")

    # We want a section
    if section is None and setting is None and default is None:
        if module_name in CONFIG:
            return CONFIG[module_name]
        else:
            return {}
    # We want one setting
    if module_name is not None and setting is not None and default is not None:
        if module_name in CONFIG and setting in CONFIG[module_name]:
            if section is None:
                return CONFIG[module_name][setting]
            else:
                return CONFIG[module_name][section][setting]
        else:
            return default
