#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    server.py
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


import socketserver
import threading
from xml.sax.saxutils import unescape

import pyotherside
from bs4 import BeautifulSoup

from squilla.lib.logger import logger
from squilla.lib import get_presence_auth_user
from squilla.lib.scheduler import send_sms_q


class PresenceServer():
    def __init__(self, auth_user=None):
        self.host = '0.0.0.0'
        self.port = 5299
        self.auth_user = auth_user
        self.server = None

    def shutdown(self):
        self.server.shutdown()
        del(self.server)
        self.server = None
        logger.debug("Presence server stopped")


    def restart(self):
        # Kill old server
        if self.server is not None:
            self.shutdown()
        # Start new one
        self.server = self.ThreadedTCPServer((self.host, self.port), self.ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

        def get_user(self, soup):
            """ Get target user ( friend cell phone number )
            """
            attrs = dict(soup.first().attrs)
            if 'to' in attrs.keys():
                if attrs['to'] != '':
                    return attrs['to']
            return False

        def handle(self):
            presence_auth_user = get_presence_auth_user()
            if presence_auth_user is None:
                return
            auth_user = presence_auth_user.get("name", None)
            recvData = self.request.recv(1024)
            # First message
            if recvData.startswith(b"<?xml version"):
                # Test if is authorized user
                soup = BeautifulSoup(recvData)
                sender = soup.find("stream:stream").get("from", None)
                if auth_user is None or not sender.startswith(auth_user + "@"):
                    logger.debug("Bonjour message received "
                                 "from unauthorized user")
                    self.request.close()
                    return

                # Get target user ( friend cell phone number)
                user = soup.find("stream:stream").get("to", None).rsplit("@", 1)[0]
                if not user:
                    # User not found
                    self.request.close()
                    return

                logger.debug("Bonjour message received "
                             "from authorized user: %s" % user)
                # First reply
                sendData = (u"""<?xml version='1.0' encoding='UTF-8'?>"""
                     u"""<stream:stream xmlns='jabber:client' """
                     u"""xmlns:stream='http://etherx.jabber.org/streams'"""
                     u""" to="%s" from="%s" version="1.0">"""
                     % (sender, user))
                self.request.sendall(sendData.encode('utf-8'))

                recvData = self.request.recv(1024)

            ###### Second msg ######
            if recvData == "<stream:features/>":
                sendData = """<stream:features />"""
                self.request.sendall(sendData.encode('utf-8'))

                recvData = self.request.recv(1024)


            if recvData.startswith(b"<message"):
                soup = BeautifulSoup(recvData)
                if not hasattr(soup, "message"):
                    self.request.close()
                    return

                sender = soup.message.get("from")
                if auth_user is None or not sender.startswith(auth_user + "@"):
                    logger.debug("Bonjour message received "
                                 "from unauthorized user")
                    self.request.close()
                    return

                if not hasattr(soup, "body"):
                    self.request.close()
                    return

                # Get target user ( friend cell phone number)
                friend = soup.message.get("to", None)
                if not friend:
                    # User not found
                    self.request.close()
                    return

                # Get Message
                message = soup.message.body.text
                message = unescape(message, {"&apos;": "'", "&quot;": '"'})

                logger.debug("New sms for %s queued" % friend)
                logger.debug("New sms content %s" % message)
                # Put message in sms queue
                if message:
                    send_sms_q.put({'to': friend,
                                    'message': message
                                    },
                                   block=False,
                                   )
                else:
                    # NOTIFY ???
                    # messag empty ????
                    pass

                
            self.request.close()


    class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        pass
