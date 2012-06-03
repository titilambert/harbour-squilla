from PyQt4 import QtCore
import Queue
from time import sleep

from friend import Friend
from lib import search_contact
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
            auth_user = {bonjour_auth_username: self.parent.bonjour_users[bonjour_auth_username]}
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
        # SMS to jabber
        print 'send sms'
        return friend.sms_to_bonjour(msg)
