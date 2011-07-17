# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtNetwork
import pybonjour
import select
import random
import dbus
import socket
from time import sleep

from lib_sms import *

port = 5299

class Friend(QtCore.QThread):
    def __init__(self, fullname, number, auth_user, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.fullname = fullname
        self.number = number
        self.port = port
        self.auth_user = auth_user

        self.parent = parent
        self.client = None # Bonjour socket client
        self.is_ready = False
        self.id = 0

    def _register_callback(self, sdRef, flags, errorCode, name, regtype, domain):
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

        self.sdRef = pybonjour.DNSServiceRegister(name = self.fullname,
                                regtype = '_presence._tcp',
                                port = self.port,
                                txtRecord = txt,
                                callBack = self._register_callback
                                )
       # Bonjour chat handcheck
        while True:
            ready = select.select([self.sdRef], [], [])
            if self.sdRef in ready[0]:
                pybonjour.DNSServiceProcessResult(self.sdRef)

    def send_sms(self, message):
        bus = dbus.SystemBus()
        smsobject = bus.get_object('com.nokia.phone.SMS', '/com/nokia/phone/SMS/ba212ae1')
        smsiface = dbus.Interface(smsobject, 'com.nokia.csd.SMS.Outgoing')
        message = str(message)
        print "send_sms"
        print message
        print "to"
        print self.number[2:].replace('+', '00')
        arr = dbus.Array(createPDUmessage(self.number[2:].replace('+', '00'), message))
        #arr = dbus.Array(createPDUmessage(self.number.replace('+', '00'), message))

        msg = dbus.Array([arr])
        while True:
            try:
                smsiface.Send(msg,'')
                break
            except dbus.exceptions.DBusException,e :
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
        so.connect((host, port))
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
        xml = u"""<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams' to="%(to)s" from="%(from)s" version="1.0">""" % dic
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
        xml = u"""<message from="%(from)s" to="%(to)s" type="chat" id="%(id)s"><body>%(msg)s</body><html xmlns="http://jabber.org/protocol/xhtml-im"><body xmlns="http://www.w3.org/1999/xhtml">%(msg)s</body></html></message>""" % dic
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
