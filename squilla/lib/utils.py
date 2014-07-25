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


import subprocess
import re

import dbus

from squilla.lib.logger import logger


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
    profile = smsiface.set_profile(profile_name)
    logger.debug("Profile is now: %s " % profile_name)

def get_ip(interface='usb'):
    # Check parameter validity
    if interface == 'usb':
       interface_name = 'rndis0'
    elif interface == 'wlan':
       interface_name = 'wlan0'
    else:
        # bad parameter
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
