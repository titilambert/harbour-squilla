import avahi
import dbus
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
from PyQt4 import QtCore


TYPE = '_presence._tcp'
class Presence_listener(QtCore.QThread):

    def __init__(self, regtype='_presence._tcp', nb_try=10, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.regtype = regtype

    def service_resolved(self, *args):
        print 'service resolved'
        print 'name:', args[2]
        print 'address:', args[7]
        print 'port:', args[8]

    def print_error(self, *args):
        print 'error_handler'
        print args[0]

    def myhandler(self, interface, protocol, name, stype, domain, flags):
        print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)

        if flags & avahi.LOOKUP_RESULT_LOCAL:
                # local service, skip
                pass

        server.ResolveService(interface, protocol, name, stype,
            domain, avahi.PROTO_UNSPEC, dbus.UInt32(0),
            reply_handler=service_resolved, error_handler=print_error)

    def run(self):
        import pdb;pdb.set_trace()
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
                'org.freedesktop.Avahi.Server')
        sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
                server.ServiceBrowserNew(avahi.IF_UNSPEC,
                    avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
                avahi.DBUS_INTERFACE_SERVICE_BROWSER)
        sbrowser.connect_to_signal("ItemNew", self.myhandler)
#        bus.add_signal_receiver(self.myhandler, path='/com/nokia/phone/SMS',
#                                dbus_interface='Phone.SMS', signal_name='IncomingSegment')
        import gobject
        from dbus import glib
        gobject.threads_init()
        glib.threads_init()
        import pdb;pdb.set_trace()
        print "EEEE"
#        gobject.MainLoop().run()


