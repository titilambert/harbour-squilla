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


import Queue
from time import sleep

from PyQt4 import QtCore

from friend import Friend
from lib import search_contact, banner_notification
from history import insert_sms_in_history

recv_sms_q = Queue.Queue()
send_sms_q = Queue.Queue()
sms_history_q = Queue.Queue()


class Scheduler(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.friend_list = []
        self.parent = parent

    def run(self):
        while True:
            sleep(1)
            if not recv_sms_q.empty():
                new_sms = recv_sms_q.get()
                status = self.sms_received(new_sms['phone_number'],
                              new_sms['message'])
                if status:
                    recv_sms_q.task_done()
            if not send_sms_q.empty():
                new_sms = send_sms_q.get()
                self.send_sms(new_sms['to'],
                              new_sms['message'])
                send_sms_q.task_done()
            if not sms_history_q.empty():
                sms = sms_history_q.get()
                insert_sms_in_history(sms)
                sms_history_q.task_done()

    def set_auth(self, bonjour_auth_user):
        bonjour_auth_username = str(bonjour_auth_user)
        if bonjour_auth_username:
            auth_user = {bonjour_auth_username:
                     self.parent.bonjour_users[bonjour_auth_username]}
            print auth_user
            for f in self.friend_list:
                f.auth_user = auth_user
        else:
            banner_notification("Avahi error, please restart HeySms")

    def send_sms(self, to, msg):
        print "send sms to ", to
        print "content ", msg
        name_list = [friend.fullname for friend in self.friend_list]
        try:
            i = name_list.index(to)
        except ValueError:
            # Impossible ?
            print "User not find in list"
        friend = self.friend_list[i]
        friend.send_sms(msg)
        sms_history_q.put({'message': msg, 'num': friend.number})

    def sms_received(self, sender, msg):
        number_list = [friend.number for friend in self.friend_list]
        print 'sms_received', sender
        if not sender in number_list:
            # Create a new friend
            print 'newfriend', sender
            fullname = search_contact(str(sender))
            name = "lastname"
            first_name = "firstname"
            number = str(sender)
            # Save it !
            bonjour_auth_username = str(self.parent.bonjour_auth_user)
            auth_user = {bonjour_auth_username:
                            self.parent.bonjour_users[bonjour_auth_username]}
            new_friend = Friend(fullname, number, auth_user)
            # append to friend il
            self.friend_list.append(new_friend)
            # Register it on bonjour
            new_friend.start()
            friend = new_friend

        else:
            i = number_list.index(sender)
            friend = self.friend_list[i]
            print "new sms from an old friend : ", friend.number
        # SMS to bonjour
        print 'send sms to bonjour'
        try:
            ret = friend.sms_to_bonjour(msg)
            print "RET", ret
            return ret
        except Exception, e:
            print "ERROR", e
            return False
