#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    lib/presence_browser.py
#
#    This file is part of HeySms
#
#    Copyright (C) 2012 Thibault Cohen
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


import socket

from mdns.zeroconf import *
import mdns

from heysms.lib.logger import logger


# wlan0 needs
# devel-su
# iwpriv wlan0 setMCBCFilter 3
zeroconf = Zeroconf(("0.0.0.0", ))
zeroconf = Zeroconf(("192.168.13.15", ))


def list_presence_contacts():
    # get entries
    raw_entries = zeroconf.cache.entries()
    # sort
    logger.debug("list_presence_contactslist_presence_contactslist_presence_contacts")
    entries = {}
    logger.debug(raw_entries)
    for entrie in raw_entries:
        name_splitted = entrie.name.rsplit("@", 1)
        if len(name_splitted) != 2:
            continue
        name, type_ = name_splitted
        logger.debug(name + " ON " + type_)
        # skip not presence service
        if not type_.endswith("._presence._tcp.local."):
            continue
        # Get data
        tmp_dict = {}
        if isinstance(entrie, mdns.zeroconf.DNSService):
            tmp_dict['server'] = entrie.server
            tmp_dict['port'] = entrie.port
            tmp_dict['name'] = name
            tmp_dict['raw_name'] = entrie.name
        else:
            continue
        # save data
        entries.setdefault(name, {}).update(tmp_dict)

    logger.debug(entries)
    return entries
