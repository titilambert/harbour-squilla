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


from squilla.lib.logger import logger

# TODO get port from config
PORT = str(5000)

def get_urls():
    s = subprocess.Popen("/sbin/ip a",
                         shell=True, stdout=subprocess.PIPE)
    output = s.stdout.readlines()
    urls = []
    tmp_dict = {}
    for line in output:
        # interface name
        m = re.match(b"^[0-9]*: (.*):.*", line)
        if m:
            interface_name = m.groups()[0].decode("utf-8")
            # Save interface
            if "ipv4" in tmp_dict or "ipv6" in tmp_dict:
                # remove loopback
                if tmp_dict['name'] != 'lo':
                    urls.append(tmp_dict)
            # New interface
            tmp_dict = {"name": interface_name}
            continue
        # ipv4
        m = re.match(b"^    inet ([0-9\.]*)/.*", line)
        if m:
            tmp_dict["ipv4"] = "http://" + m.groups()[0].decode("utf-8") + ":" + PORT
            continue
        # ipv6
        m = re.match(b"^    inet6 ([a-fA-F0-9:]*)/.*", line)
        if m:
            tmp_dict["ipv6"] = "http://" + m.groups()[0].decode("utf-8") + ":" + PORT

    # Save last interface if needed
    if "ipv4" in tmp_dict or "ipv6" in tmp_dict:
        urls.append(tmp_dict)

    return urls
