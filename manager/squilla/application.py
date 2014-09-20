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
#from squilla.lib.config import get_silent_mode, get_interface_name
from squilla.lib.logger import logger
from squilla.lib.scheduler import Scheduler
#from squilla.lib.utils import get_current_profile, set_current_profile, get_current_usb_mode, set_current_usb_mode
#from squilla.lib.sms_listener import Sms_listener
#from squilla.lib.utils import configure_interface

class Application:
    def __init__(self, interval):
        self.sms_listener = None
        self.scheduler = None
        self.presence_server = None
        self.first_profile = None
        self.last_usb_mode = None

    #/home/nemo/.local/share/system/privileged/Contacts/qtcontacts-sqlite/contacts.db
    def start(self):
        logger.set_debug(True)
        logger.debug("Application started")

        # start scheduler
        self.scheduler = Scheduler()
        self.scheduler.start()


    def stop(self):
        logger.debug("Application stopping")
        # Stop scheduler
        self.scheduler.shutdown()
