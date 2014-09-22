#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    application.py
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


import sys

from mdns.zeroconf import Zeroconf

from squilla.libs.logger import logger

from .lib.config import get_silent_mode, get_interface_name, get_bridges
from .lib.utils import get_current_profile, set_current_profile, get_current_usb_mode, set_current_usb_mode
from .lib.sms_listener import Sms_listener
from .lib.scheduler import Scheduler
from .lib.presence_browser import list_presence_contacts, presence_auth_user, set_zeroconf
from .lib.server import PresenceServer
from .lib.friend import friend_list, delete_friend
from .lib.utils import configure_interface, get_interface_address
from .config import get_favorites







class Application:
    def __init__(self, interval):
        self.started = False
        self.sms_listener = None
        self.scheduler = None
        self.presence_server = None
        self.last_profile = None
        self.last_usb_mode = None
        self.zeroconf = None
        self.selected_interface = None

    #/home/nemo/.local/share/system/privileged/Contacts/qtcontacts-sqlite/contacts.db
    def start(self):
        logger.set_debug(True)
        logger.debug("Application starting")
        # Get which bridges we need to run
        self.bridges = get_bridges()

        # Get selected interface (usb or wifi)
        self.selected_interface = get_interface_name()
        # get current usb mode
        if self.selected_interface == 'usb':
            self.last_usb_mode = get_current_usb_mode()
        configure_interface(selected_interface)

        # start sms_listener
        self.sms_listener = Sms_listener(self)
        self.sms_listener.start()

        # Load favorite friends
        self.favorite_friends = get_favorites()

        # Go in silent mode
        if get_silent_mode():
            self.last_profile = get_current_profile()
            set_current_profile('silent')
            logger.debug("Switch to silent mode")

        # For Bonjour bridge
        if 'bonjour' in self.bridges:
            # Set Zeroconf
            interface_address = get_interface_address(selected_interface)
            if interface_address is None:
                interface_address = '0.0.0.0'
            self.zeroconf = Zeroconf((interface_address, ))
            # start presencer server
            self.presence_server = PresenceServer(self)
            self.presence_server.restart()

        # start scheduler
        self.scheduler = Scheduler(self)
        self.scheduler.start()

        # Started
        logger.debug("Application started")
        self.started = True

    def stop(self):
        logger.debug("Application stopping")
        # For Bonjour bridge
        if 'bonjour' in self.bridges:
            # Unregister all services
            tmp_friend_list = friend_list[:]
            for friend in tmp_friend_list:
                delete_friend(friend.number)
            # Stop presence server
            self.presence_server.shutdown()

        # Check sms listener
        if not self.sms_listener.is_alive():
            logger.debug("SMS listener is stopped")
        # Stop scheduler
        self.scheduler.shutdown()

        # Switch back profile
        if get_silent_mode():
            set_current_profile(self.last_profile)
            logger.debug("Switch back profile")
        # Switch back USB mode
        if self.selected_interface == 'usb' and self.last_usb_mode is not None:
            set_current_usb_mode(self.last_usb_mode)

        # Stopped
        self.started = False
