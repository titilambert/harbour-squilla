#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    lib/presence_browser.py
#
#    This file is part of Squilla
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

from mdns.zeroconf import DNSAddress
import mdns

from squilla.lib import presence_auth_user, presence_users, friend_list
from squilla.lib.logger import logger
from mdns.zeroconf import Zeroconf


# wlan0 needs
# devel-su
# iwpriv wlan0 setMCBCFilter 3
#zeroconf = Zeroconf(("0.0.0.0", ))
zeroconf = Zeroconf(("192.168.13.15", ))


#presence_auth_user = None
#presence_users = {}

def list_presence_contacts():
    #import pdb;pdb.set_trace()
    # https://github.com/svinota/mdns/issues/8
    # get entries
    raw_entries = zeroconf.cache.entries()
    # sort
    entries = {}
    host_ip = {}
    for entry in raw_entries:
        logger.debug("Raw entry:" + str(entry))
        if isinstance(entry, DNSAddress):
            # entry.family = 4|6 (IPv4|IPv6)
            # TODO: IPv6 support
            if entry.family == 4:
                host_ip[entry.name] = entry._address()
            continue
        name_splitted = entry.name.rsplit("@", 1)
        if len(name_splitted) != 2:
            continue
        name, type_ = name_splitted
        logger.debug(name + " ON " + type_)
        # skip not presence service
        if not type_.endswith("._presence._tcp.local."):
            continue
        # Get data
        tmp_dict = {}
        if isinstance(entry, mdns.zeroconf.DNSService):
            tmp_dict['hostname'] = entry.server
            tmp_dict['port'] = entry.port
            tmp_dict['name'] = name
            tmp_dict['raw_name'] = entry.name
        else:
            continue
        # save data
        entries.setdefault(name, {}).update(tmp_dict)

    # Get host ip
    for entry in entries.values():
        entry['host'] = host_ip.get(entry['hostname'], None)
    # Delete all entries which have not ip
    friend_name_list = [f.fullname for f in friend_list]
    entries = dict([(name, entry) for name, entry in entries.items()
                    if entry['host'] != None and name not in friend_name_list])

    logger.debug("Entries: " + str(entries))
    # Save presences users
    save_presence_users(entries)
    # Set presence auth user with the only one entry
    if len(entries) == 1:
        lonely_presense_auth_user = list(entries.keys())[0]
        set_presence_auth_user(lonely_presense_auth_user)

    return entries


def save_presence_users(entries):
    global presence_users
    presence_users = entries.copy()


def set_presence_auth_user(selected_presence):
    logger.debug("Set auth user: " + str(selected_presence))
    global presence_users
    global presence_auth_user
    presence_auth_user = presence_users.get(selected_presence, None)
    print(presence_auth_user)


def load_presences(selected_presence=None):
    """ Load presence list
    If selected_presence is set
    it will be the first of the list
    """
    presences = list_presence_contacts()

    ret = []

    # Prepare the first element of the combobox
    if selected_presence is not None and selected_presence in presences:
        ret.append({'name': selected_presence,
                    'value': presences.get(selected_presence)
                    })

    # Complete the combobox
    for name, data in presences.items():
        if selected_presence != name:
            ret.append({'name': name, 'data': data})

    return ret
