#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    utils.py
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
import subprocess
import re

import dbus

from squilla.libs.logger import logger
from .config import get_interface_name



last_usb_mode = 'charging_only'


def get_current_profile():
    # dbus-send --type=method_call --print-reply --dest=com.nokia.profiled /com/nokia/profiled com.nokia.profiled.get_profile
    logger.debug("Get current profile")
    bus = dbus.SessionBus()
    smsobject = bus.get_object('com.nokia.profiled',
                               '/com/nokia/profiled',
                               False)
    smsiface = dbus.Interface(smsobject, 'com.nokia.profiled')
    profile_name = smsiface.get_profile()
    logger.debug("Current profile: %s" % profile_name)
    return profile_name


def set_current_profile(profile_name):
    # dbus-send --type=method_call --print-reply --dest=com.nokia.profiled /com/nokia/profiled com.nokia.profiled.set_profile string:"silent"
    logger.debug("Setting profile to %s:" % profile_name)
    bus = dbus.SessionBus()
    smsobject = bus.get_object('com.nokia.profiled',
                               '/com/nokia/profiled',
                               False)
    smsiface = dbus.Interface(smsobject, 'com.nokia.profiled')
    profile = smsiface.set_profile(str(profile_name))
    logger.debug("Profile is now: %s " % profile_name)

def get_interface_address(interface='usb'):
    # Check parameter validity
    if interface == 'usb':
       interface_name = 'rndis0'
    elif interface == 'wifi':
       interface_name = 'wlan0'
    else:
        # bad parameter
        logger.debug("Get IP error: Bad interface name %s" % interface)
        return None

    s = subprocess.Popen("/sbin/ip a",
                         shell=True, stdout=subprocess.PIPE)
    output = s.stdout.readlines()
    lines =[l.strip() for l in output
            if l.strip().decode('utf-8').endswith(interface_name)]
    if len(lines) == 0:
        logger.debug("%s not connected" % interface)
    elif len(lines) > 1:
        # Impossible
        logger.debug("More than one %s detected ???" % interface)
    else:
        logger.debug("USB seems connected")
        line = lines[0]
        match = re.search(b"inet ([0-9.]*)/[0-9]* brd", line)
        if match is not None:
            address_ip = match.group(1).decode('utf-8')
            logger.debug("%s address ip: %s" % (interface, address_ip))
            return address_ip


def configure_interface(interface):
    global last_usb_mode
    if interface not in ['usb', 'wifi']:
        logger.debug("Unable to determine which interface I have to use")
        return False

    elif interface == 'wifi':
        return True
        command = subprocess.Popen("/sbin/iwpriv wlan0 setMCBCFilter 3",
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        output = command.stdout.readlines()
        error = command.stderr.readlines()
        if error:
            logger.debug("Error during wlan configuration: %s" % str(error))
    else:
        set_current_usb_mode('developer_mode')


def get_current_usb_mode():
    # Get current mode
    command = subprocess.Popen("usb_moded_util -q",
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output = command.stdout.readlines()
    error = command.stderr.readlines()
    if error:
        logger.debug("Error getting USB mode: %s" % str(error))
        return 'developer_mode'
    if len(output) != 1:
        logger.debug("Unable to determine current USB mode")
        return 'developer_mode'
    match = re.match(b"mode = (.*)", output[0].strip())
    if match is None:
        # not match, possible ???
        logger.debug("Unable to determine current USB mode")
        return 'developer_mode'
    # Save last usb mode
    usb_mode = match.group(1)
    return usb_mode.decode('utf-8')


def set_current_usb_mode(mode):
    if not isinstance(mode, str):
        mode = mode.decode('utf-8')
    if mode not in ['charging_only', 'pc_suite', 'developer_mode']:
        logger.debug("Bad USB mode: %s" % mode)
        return False
    # Go to developer usb mode
    command = subprocess.Popen("usb_moded_util -s %s" % mode,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output =  command.stdout.readlines()
    error = command.stderr.readlines()
    if error:
        logger.debug("Error setting USB mode: %s" % str(error))
        return False
    logger.debug("USB mode is now: %s" % mode)
    return True
