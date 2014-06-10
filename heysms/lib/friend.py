#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    friend.py
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


from threading import Thread


port = 5299
ip_address = '192.168.2.38'


class Friend(Thread):
    def __init__(self, fullname, number, auth_user, parent=None):
        Thread.__init__(self)
        self.fullname = fullname
        self.number = number
        self.port = port
        self.ip_address = ip_address
        self.auth_user = auth_user
        self.node = "%s@jolla" % ''.join(c for c in self.fullname if c.isalnum()).lower()
        self.favorite = False

        self.parent = parent
        self.client = None  # Bonjour socket client
        self.is_ready = False
        self.id = 0

    def set_data(self, value, attr):
        """ For view
        """
        if attr == "favorite":
            value, bool = value.toInt()
            if bool:
                if value == QtCore.Qt.Checked:
                    setattr(self, "favorite", QtCore.Qt.Checked)
                else:
                    setattr(self, "favorite", QtCore.Qt.Unchecked)

                return True
        return False

    def run(self):
        # Register on bonjour chat
        self.id = random.randint(100000000000, 999999999999)
        txt = {}
        txt['1st'] = self.fullname
        txt['last'] = ""
        txt['status'] = 'avail'
        txt['port.p2pj'] = self.port
        txt['nick'] = self.fullnick
        #txt['node'] = self.node
        txt['jid'] = self.node
        txt['email'] = self.node
        txt['version'] = 1
        txt['txtvers'] = 1

        regtype = '_presence._tcp.local.'
        node = ".".join((self.node, regtype))
        info = ServiceInfo(regtype,
                           node,
                           inet_aton(self.ip_address),
                           self.port,
                           properties=txt)
        r.register_service(info)
        r.engine.join()

