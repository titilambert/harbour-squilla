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

        msg = deoctify(msgarray)

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

