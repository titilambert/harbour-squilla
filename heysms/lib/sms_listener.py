#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    sms_listener.py
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


import time

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from PyQt4 import QtCore
from math import ceil

from lib_sms import createPDUmessage, deoctify, deoctify_int
from scheduler import recv_sms_q
from lib import logger


class Sms_listener(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent

    def callback(self, pdumsg, msgcenter, somestring, sendernumber):
        logger.debug("New sms received")

        firstoctet = int(pdumsg[0])
        if firstoctet & 0x03:
            logger.debug("invalid SMS-DELIVER PDU, TP-MTI not cleared.")
            return

        if firstoctet & 0x40:
            logger.debug("message has user data header (multipart sms), not yet supported.")

        # construct pointer to TP-PID (protocol identifier).
        # We've got: first octet + address length (sender) + type of address
        # i.e. 3 bytes + the address itself (length specified in digits)
        ptr = 3 + int(ceil(float(pdumsg[1]) / 2))
        tp_dcs = int(pdumsg[ptr + 1])
        tp_udl = int(pdumsg[ptr + 9])

        msgarray = pdumsg[ptr + 10 : len(pdumsg)]

        # test for international msg
        if tp_dcs == 8:
            logger.debug("International sms received")
            msg = deoctify_int(msgarray)
        else:
            logger.debug("local sms received")
            msg = deoctify(msgarray)

        if msg > 0:
            logger.debug("Sms from: %s" % sendernumber)
            logger.debug("Sms content: %s" % msg)

        recv_sms_q.put({'phone_number': sendernumber,
                        'message': msg})

    def run(self):
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        bus.add_signal_receiver(self.callback,
                                path='/com/nokia/phone/SMS',
                                dbus_interface='Phone.SMS',
                                signal_name='IncomingSegment')
        import gobject
        from dbus import glib
        gobject.threads_init()
        glib.threads_init()
