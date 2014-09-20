#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    scheduler.py
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


import queue
from threading import Thread
from time import sleep

import pyotherside

from squilla.lib.logger import logger
from squilla.lib.config import get_authentication
from squilla.lib.daemon_manager import daemon_is_running
from squilla.lib.utils import get_urls


class Scheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.must_run = False

    def shutdown(self):
        logger.debug("Stopping Scheduler")
        self.must_run = False

    def run(self):
        self.must_run = True
        while self.must_run:
            sleep(2)
            # Get ip addresses
            interfaces = get_urls()
            pyotherside.send('show_interfaces', interfaces)
            # Get authentication
            auth = get_authentication()
            pyotherside.send('show_authentication', auth)
            # Get daemon status
            running = daemon_is_running()
            pyotherside.send('show_daemon_status', running)
        logger.debug("Scheduler stopped")

