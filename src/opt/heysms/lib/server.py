#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    server.py
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


import socket
from PyQt4 import QtCore
from time import sleep
from BeautifulSoup import BeautifulSoup 

from scheduler import send_sms_q
 
class Bonjour_server():
    def __init__(self, auth_user):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '0.0.0.0'
        self.port= 5299
        self.maxClient = 999
        self.running = True
        self.auth_user = auth_user
        self.thread = self.Thread(self)

    def get_user(self, soup):
        """ Get target user ( friend cell phone number )
        """
        attrs = dict(soup.first().attrs)
        if 'to' in attrs.keys():
            if attrs['to'] != '':
                return attrs['to']
        return False

    def check_auth(self, soup):
        """ Check bonjour sender username
        """
        attrs = dict(soup.first().attrs)
        if 'from' in attrs.keys():
            if attrs['from'] == self.auth_user:
                return True
        return False

    def set_auth(self, username):
        """ Set bonjour user which receive and send sms
        """
        self.auth_user = username

    def listen(self):
        self.thread.start()

    def is_running(self):
        return self.thread.isRunning()

    def stop(self):
        self.thread.shutdown()

    class Thread(QtCore.QThread):
        def __init__(self, parent):
            QtCore.QThread.__init__(self)
            self.parent = parent
            self.server = self.parent.server
            self.host = self.parent.host
            self.port = self.parent.port
            self.maxClient = self.parent.maxClient
            self.setTerminationEnabled(True)

        def shutdown(self):
            self._isrunning = False
            self.server.close()
            self.quit()

        def run(self):
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            i = 0
            while True:
                try:
                    self.server.bind((str(self.host), int(self.port + i)))
                except socket.error, e:
                    if e[0] == '98':
                        i = i + 1
                        continue
                print "PORT :", self.port + i
                break;
                
            self.server.listen(int(self.maxClient))
            self._isrunning = True
#            try:
            while self._isrunning:
#                self.server.settimeout(5)
#                try:
#                    print "Waiting"
                channel, details = self.server.accept()
#                except socket.timeout, e:
#                    continue
                channel.setblocking( 1 )
                print "Waiting2"
                recvData = channel.recv(2000)
                print "=======rec1==========="
                if recvData.startswith("<?xml version"):
                    # Test if is authorized user
                    soup = BeautifulSoup(recvData)
                    if not self.parent.check_auth(soup):
#                        print "Unauth user"
                        channel.close()
                        continue
                    #print "auth_user ",self.parent.auth_user
                    self.auth_user = self.parent.auth_user

                    # Get target user ( friend cell phone number)
                    user = self.parent.get_user(soup)
                    if user == False:
                        channel.close()
                        continue
#                    print user

                    # First reply
                    sendData = u"""<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams' to="%s" from="%s" version="1.0">""" % (self.auth_user, user)
#                    print "senddata ", sendData
                    channel.send(sendData.encode('utf-8'))

                    recvData = channel.recv(2000)
#                    print recvData

#                print "=================="
                if recvData == "<stream:features/>":
                    #sendData = """<stream:features id="164130694186"/>"""
                    sendData = """<stream:features />"""
                    channel.send(sendData)

                #sendData = """<stream:features id="164130694186"/>"""
                #channel.send(sendData)

#                print "=================="
                    recvData = channel.recv(2000)
#                print recvData
                if recvData.startswith("<message"):
                    soup = BeautifulSoup(recvData)
                    if not self.parent.check_auth(soup):
#                        print "Unauth user"
                        channel.close()
                        continue
                    # Get user whowill receive sms
                    user = self.parent.get_user(soup)
                    # Get Message
                    root = soup.first()
                    message = root.findChild('body').getString()

                    print user
                    print "new_message to ", user
                    print "new_message content ", message
                    # Put message in sms queue
                    send_sms_q.put({'to': user,
                               'message': message
                               })
#                print recvData

                channel.close()

#        except Exception, e:
#            print e
#            channel.close()
#            self.server.close()


#bs = Bonjour_server()
#bs.listen()
