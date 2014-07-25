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
from squilla.lib.config import get_silent_mode
from squilla.lib.logger import logger
from squilla.lib.utils import get_current_profile, set_current_profile, get_ip
from squilla.lib.sms_listener import Sms_listener
from squilla.lib.scheduler import Scheduler
from squilla.lib.presence_browser import list_presence_contacts, presence_auth_user
from squilla.lib.server import PresenceServer
from squilla.lib.friend import load_favorite_friends, friend_list, delete_friend

class Application:
    def __init__(self, interval):
        self.sms_listener = None
        self.scheduler = None
        self.presence_server = None
        self.first_profile = None

    #/home/nemo/.local/share/system/privileged/Contacts/qtcontacts-sqlite/contacts.db
    def start(self):
        logger.set_debug(True)
        logger.debug("Application started")
        self.sms_listener = Sms_listener()
        self.sms_listener.start()
        self.scheduler = Scheduler()
        self.scheduler.start()
        self.presence_server = PresenceServer()
        self.presence_server.restart()
        load_favorite_friends()
        if get_silent_mode():
            self.first_profile = get_current_profile()
            set_current_profile('silent')
            logger.debug("Switch to silent mode")
            

    def stop(self):
        logger.debug("Application stopping")
        print(friend_list)
        # Unregister all services
        tmp_friend_list = friend_list[:]
        for friend in tmp_friend_list:
            delete_friend(friend.number)
        # Check sms listener
        if not self.sms_listener.is_alive():
            logger.debug("SMS listener is stopped")
        # Stop scheduler
        self.scheduler.shutdown()
        # Stop presence server
        self.presence_server.shutdown()
        # Swith back profile
        if get_silent_mode():
            set_current_profile(self.first_profile)
            logger.debug("Switch back profile")
