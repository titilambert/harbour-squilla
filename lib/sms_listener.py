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


import sched, time                
import dbus                       
from dbus.mainloop.glib import DBusGMainLoop
from PyQt4 import QtCore

from lib_sms import *

from scheduler import recv_sms_q

class Sms_listener(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent

    def callback(self, pdumsg, msgcenter, somestring, sendernumber):

        msglength = int(pdumsg[18])
        msgarray = pdumsg[19:len(pdumsg)]

        msg =  deoctify(msgarray)

        if msg > 0:
           print 'New message received from', sendernumber
           print 'new_message', msg

        recv_sms_q.put({'phone_number': sendernumber,
                        'message': msg})

    def run(self):
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus() #should connect to system bus instead of session because the former is where the incoming signals come from
        bus.add_signal_receiver(self.callback, path='/com/nokia/phone/SMS', dbus_interface='Phone.SMS', signal_name='IncomingSegment')
        import gobject
        from dbus import glib
        gobject.threads_init()
        glib.threads_init()

