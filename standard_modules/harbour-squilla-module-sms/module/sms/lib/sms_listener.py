#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    sms_listener.py
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


import time
from threading import Thread

import dbus
from dbus import glib
from dbus.mainloop.glib import DBusGMainLoop

from squilla.libs.logger import logger
from .scheduler import sms_received_q


class Sms_listener(Thread):
    def __init__(self, application):
        Thread.__init__(self)
        self.application = application 

    def callback(self, pdumsg, msgcenter, somestring, sendernumber):
        logger.debug("New sms received: " + somestring)

    def handle_sms(self, message, data):
        sendernumber = data.get(dbus.String('Sender'), None)
        sendtime = data.get(dbus.String('SentTime'), None)
        logger.debug('New message from %s, at %s: %s' % (sendernumber,
                                                         sendtime,
                                                         message))
        recv_sms_q.put({'phone_number': sendernumber,
                        'message': message,
                        },
                        block=False,
                       )

    def run(self):
        logger.debug("run sms_listener")
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        bus.add_signal_receiver(self.handle_sms, path='/ril_0',   dbus_interface='org.ofono.MessageManager', signal_name='IncomingMessage')
        glib.threads_init()
