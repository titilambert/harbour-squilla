#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    friend.py
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


import select
import random
import socket
from time import sleep
import subprocess
from socket import inet_aton
from threading import Thread

import pyotherside

from mdns.zeroconf import ServiceInfo
import dbus

from squilla.lib.logger import logger
from squilla.lib.config import is_favorite, get_favorites
from squilla.lib import get_presence_auth_user, friend_list
from squilla.lib.presence_browser import zeroconf


port = 5299
# NEED TO GET THE GOOD IP!!!!
ip_address = '192.168.13.15'
#ip_address = '0.0.0.0'


class Friend(Thread):
    def __init__(self, fullname, number, auth_user, parent=None):
        Thread.__init__(self)
        self.fullname = fullname
        self.number = number
        self.port = port
        self.ip_address = ip_address
        self.auth_user = auth_user
        self.node = "%s@jolla" % fullname
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
        self.id = random.randint(0, 10000000)
        # Prepare properties
        txt = {}
        txt['1st'] = str(self.fullname)
        txt['last'] = ""
        txt['status'] = 'avail'
        txt['port.p2pj'] = 5299
        txt['nick'] = str(self.fullname)
        txt['node'] = self.node
        txt['jid'] = str(self.node)
        txt['email'] = str(self.node)
        txt['version'] = 1
        txt['txtvers'] = 1
        name = self.node + '._presence._tcp.local.'
        reg_type = '_presence._tcp.local.'

        # Prepare service informations
        self.info = ServiceInfo(reg_type, name, inet_aton(self.ip_address), self.port, properties=txt)
        # Register service
        zeroconf.register_service(self.info)
        self.is_ready = True
        # Join thread
        zeroconf.engine.join()

    def unregister(self):
        """ Unregister service """
        zeroconf.unregister_service(self.info)

    def send_sms(self, message):
        logger.debug("Sending sms using 'dbus'")
        bus = dbus.SystemBus()
        smsobject = bus.get_object('org.ofono',
                                   '/ril_0')
        smsiface = dbus.Interface(smsobject, 'org.ofono.MessageManager')
        message = message.encode('utf-8')
        smsiface.SendMessage(self.number, message)
        logger.debug("Sms send: %s" % message)
        logger.debug("to: %s " % self.number)

    def sms_to_bonjour(self, msg):
        logger.debug("Forward sms to bonjour")
        msg = msg.replace("<", "&lt;")
        msg = msg.replace(">", "&gt;")
        # Waiting self is bonjour registered
        while self.is_ready == False:
            logger.debug("Waiting bonjour contact "
                         "registered: %s" % self.fullname)
            sleep(1)

        # Connect to bonjour server
        self.auth_user = get_presence_auth_user()
        if self.auth_user is None:
            logger.debug("Authentication user not set")
            return False
        #logger.debug(self.auth_user)
        #logger.debug(self.auth_user.values())
        #logger.debug(list(self.auth_user.values()))
        host = self.auth_user['host']
        port = self.auth_user['port']
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug("Connecting to %s:%s" % (host, port))
        try:
            so.connect((host, port))
        except TypeError as e:
            logger.debug("Connection error: %s" % str(e))
            return False
        # Dont need this !?
        so.setblocking(1)
        so.settimeout(2)

        # Prepare variables
        username = self.auth_user['name']
        dic = {"to": username,
               "from": self.node,
               "msg": msg,
               "id": self.id}
        # Hand check
        # Send data
        xml = (u"""<?xml version='1.0' encoding='UTF-8'?><stream:stream """
               u"""xmlns='jabber:client' """
               u"""xmlns:stream='http://etherx.jabber.org/streams' """
               u"""to="%(to)s" from="%(from)s" version="1.0">""" % dic)
        logger.debug(xml)
        so.send(xml.encode('utf-8'))

        # Read data
        try:
            data = so.recv(1024)
        except socket.timeout:
            logger.debug("socket.timeout1")
        except Exception as e:
            logger.debug(e)

        # Send data
        so.send("""<stream:features/>""".encode('utf-8'))

        # Read data
        try:
            data = so.recv(1024)
        except socket.timeout:
            logger.debug("socket.timeout2")

        # Send data
        xml = ("""<message from="%(from)s" to="%(to)s" type="chat" """
               """id="%(id)s"><body>%(msg)s</body></message>""" % dic)
        logger.debug(xml)
        logger.debug("Send message")
        so.send(xml.encode('utf-8'))
        try:
            data = so.recv(1024)
        except socket.timeout:
            logger.debug("socket.timeout3")
        # Close connection
        logger.debug("End foward sms to bonjour")
        so.close()
        return True


def delete_friend(number):
    global friend_list
    for friend in friend_list:
        if friend.number == number:
            logger.debug("Friend %s deleted" % friend.fullname)
            index = friend_list.index(friend)
            friend_list.remove(friend)
            friend.unregister()
            del(friend)
            return index
    return None


def add_friend(fullname, number):
    global friend_list
    number_list = [friend.number for friend in friend_list]
    if not number in number_list:
        # Create a new friend
        logger.debug("This is a new friend: %s" % number)
        # Save it !
        logger.debug("PRESENCE_AUTH: " + str(get_presence_auth_user()))
        auth_user = get_presence_auth_user()
        new_friend = Friend(fullname, number, auth_user)
        # append to friend list
        friend_list.append(new_friend)
        # Register it on bonjour
        new_friend.start()
        tmp_dict = {'name': new_friend.fullname,
                    'favorite': is_favorite(number),
                    'number': new_friend.number}
        # Add friend in listmodel
        pyotherside.send('add_friend_list', tmp_dict)


def load_favorite_friends():
    favorites = get_favorites()
    for number, name in favorites:
        if number and name:
            add_friend(name, number)
