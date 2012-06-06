#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    friend.py
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


import select
import random
import socket
from time import sleep

import dbus
from PyQt4 import QtCore, QtNetwork

import pybonjour
from lib_sms import createPDUmessage
from country_code import country_code

port = 5299


class Friend(QtCore.QThread):
    def __init__(self, fullname, number, auth_user, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.fullname = fullname
        self.number = number
        self.port = port
        self.auth_user = auth_user

        self.parent = parent
        self.client = None  # Bonjour socket client
        self.is_ready = False
        self.id = 0

    def _register_callback(self, sdRef, flags, errorCode,
                           name, regtype, domain):
        # Set variable when sel is registered
        sleep(1)
        self.is_ready = True
        print "Registered", self.fullname

    def run(self):
        # Register on bonjour chat
        self.id = random.randint(100000000000, 999999999999)
        txt = {}
        txt['status'] = 'avail'
        txt['port.p2pj'] = self.port
        txt['version'] = 1
        txt['txtvers'] = 1

        txt = pybonjour.TXTRecord(txt, strict=True)

        self.sdRef = pybonjour.DNSServiceRegister(name=self.fullname,
                                regtype='_presence._tcp',
                                port=self.port,
                                txtRecord=txt,
                                callBack=self._register_callback
                                )
       # Bonjour chat handcheck
        while True:
            ready = select.select([self.sdRef], [], [])
            if self.sdRef in ready[0]:
                pybonjour.DNSServiceProcessResult(self.sdRef)

    def send_sms(self, message):
        bus = dbus.SystemBus()
        smsobject = bus.get_object('com.nokia.phone.SMS',
                                   '/com/nokia/phone/SMS/ba212ae1')
        smsiface = dbus.Interface(smsobject, 'com.nokia.csd.SMS.Outgoing')
        message = message.encode('utf-8')
        print "send_sms"
        print message
        print "to"
        print self.number
        print self.number[1:]
        if self.number.startswith("+"):
            for code in country_code:
                if self.number[1:].startswith(code):
                    print "CODE", code
                    print self.number.split(code,1)
                    print self.number.split(code,1)[-1]
                    number = self.number.split(code,1)[-1]
        arr = dbus.Array(createPDUmessage(number,
                                          message))

        msg = dbus.Array([arr])
        while True:
            try:
                smsiface.Send(msg, '')
                print "sms sent"
                break
            except dbus.exceptions.DBusException, e:
                print e
                print "sending sms failed, retry"
                pass
        print "end sending"

    def sms_to_bonjour(self, msg):
        # Waiting self is bonjour registered
        while self.is_ready == False:
            print "waiting"
            sleep(1)

        #print "QQQ"
        # Connect to bonjour server
        host = self.auth_user.values()[0]['host']
        port = self.auth_user.values()[0]['port']
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            so.connect((host, port))
        except TypeError,e :
            print "Type Error", e
            return False
        # Dont need this !?
        so.setblocking(1)
        so.settimeout(2)

        # Prepare variables
        username = self.auth_user.keys()[0]
        dic = {"to": username,
               "from": self.fullname,
               "msg": msg,
               "id": self.id}
        # Hand check
        # Send data
        xml = (u"""<?xml version='1.0' encoding='UTF-8'?><stream:stream """
               u"""xmlns='jabber:client' """
               u"""xmlns:stream='http://etherx.jabber.org/streams' """
               u"""to="%(to)s" from="%(from)s" version="1.0">""" % dic)
        so.send(xml.encode('utf-8'))

        # Read data
        try:
            data = so.recv(1024)
            #print data
        except socket.timeout:
            #print "socket.timeout"
            pass

        # Send data
        so.send("""<stream:features/>""")

        # Read data
        try:
            data = so.recv(1024)
            #print data
        except socket.timeout:
            #print "socket.timeout"
            pass

        # Send data
        xml = (u"""<message from="%(from)s" to="%(to)s" type="chat" """
               u"""id="%(id)s"><body>%(msg)s</body><html """
               u"""xmlns="http://jabber.org/protocol/xhtml-im"><body """
               u"""xmlns="http://www.w3.org/1999/xhtml">%(msg)s</body>"""
               u"""</html></message>""" % dic)
        so.send(xml.encode('utf-8'))
        print "LAST"
        try:
            data = so.recv(1024)
            #print data
        except socket.timeout:
            #print "socket.timeout"
            pass
        # Close connection
        so.close()
        return True
