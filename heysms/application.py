#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    application.py
#
#    This file is part of HeySms
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
from heysms.lib.logger import logger
from heysms.lib.sms_listener import Sms_listener
from heysms.lib.scheduler import Scheduler
from heysms.lib.presence_browser import list_presence_contacts

class Application:
    def __init__(self, interval):
        pass

    #/home/nemo/.local/share/system/privileged/Contacts/qtcontacts-sqlite/contacts.db
    def start(self):
        logger.set_debug(True)
        logger.debug("Application started")
        sms_listener = Sms_listener()
        sms_listener.start()
        scheduler = Scheduler()
        scheduler.start()
