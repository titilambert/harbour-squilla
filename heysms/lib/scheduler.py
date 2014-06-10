#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    scheduler.py
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

import queue
from threading import Thread
from time import sleep

from heysms.lib.logger import logger
from heysms.lib.friend import Friend

recv_sms_q = queue.Queue()


class Scheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.friend_list = []
        self.must_run = False
        self.waiting_authorized_contact = False

    def run(self):
        self.must_run = True
        while self.must_run:
            sleep(0.1)
            if not recv_sms_q.empty():
                new_sms = recv_sms_q.get()
                status = self.sms_received(new_sms['phone_number'],
                              new_sms['message'])
                if status:
                    recv_sms_q.task_done()

    def sms_received(self, sender, msg):
        logger.debug("New sms from: %s" % sender)
        self.number_list = [friend.number for friend in self.friend_list]
        if not sender in self.number_list:
            # Create a new friend
            logger.debug("This is a new friend: %s" % sender)
            fullname = search_contact_by_number(str(sender))
            number = str(sender)
            # Save it !
            bonjour_auth_username = str(self.parent.bonjour_auth_user)
            auth_user = {bonjour_auth_username:
                            self.parent.bonjour_users[bonjour_auth_username]}
            new_friend = Friend(fullname, number, auth_user)
            # Add to friend list in table model
            self.parent.central_widget.friends_list.emit(QtCore.SIGNAL("add_friend"), new_friend)
            # append to friend list
            self.friend_list.append(new_friend)
            # Register it on bonjour
            new_friend.start()
            friend = new_friend
        else:
            i = self.number_list.index(sender)
            friend = self.friend_list[i]
            logger.debug("This is an old friend: %s" % sender)
        # SMS to bonjour
        logger.debug("Forward sms to bonjour")
        try:
            ret = friend.sms_to_bonjour(msg)
            logger.debug("sms_to_bonjour return: %s" % str(ret))
            return ret
        except Exception(e):
            logger.debug("sms_to_bonjour error: %s" % str(e))
            return False

