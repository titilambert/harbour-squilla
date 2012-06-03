#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    lib.py
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
import socket
from time import sleep
import bsddb
import re
import osso

import dbus, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

import pybonjour

debug = True


def search_contact(phone_number):
    db = bsddb.hashopen('/home/user/.osso-abook/db/addressbook.db', 'r')
    ret = phone_number.replace("+",'')
    for contact in db.values():
        if contact.find(phone_number) != -1:
            tmp = contact.split("FN:")
            if len(tmp) > 1:
                tmp = tmp[1].split("\r\n")
                if len(tmp) > 1:
                    ret = tmp[0]
                    print tmp[0]
            break

    ret = ret.decode('utf-8')
    print type(ret)

    print "contact name : ", ret
    return ret
            


def search_contact_py_osso_abook(phone_number):
    from python_osso_abook.addressbook import AddressBook
    import gobject

    gobject.threads_init()
    loop = gobject.MainLoop()

    result = list()
    abook = AddressBook.get_default()

    def callback(contacts):
        print "QQQ"
        result.extend(contacts)
        loop.quit()

    def run():
        print "EEE"
        abook.find_contacts_for_phone_number(phone_number, True, callback)
        print "RRR"
    abook.find_contacts_for_phone_number(phone_number, True, callback)
    gobject.idle_add(run)
    loop.run()
    print len(result)


def resolve(name, interface):
    import gobject
    TYPE = '_presence._tcp'
    global ret
    ret = None

    def service_resolved(*args):
        global ret
        #print 'service resolved'
        #print 'name:', args[2]
        #print 'address:', args[7]
        #print 'port:', args[8]
        ret = "%s" % args[7]
        if ret.find('.') == -1:
            ret = None
        ml.quit()

    def print_error(*args):
        #print 'error_handler'
        #print args[0]
        ml.quit()
     
    def myhandler(interface, protocol, name, stype, domain, flags):
        #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)

        print flags
        print avahi.LOOKUP_RESULT_LOCAL
        print 'WWWW'
        if flags & avahi.LOOKUP_RESULT_LOCAL:
                # local service, skip
                ml.quit()

        server.ResolveService(interface, protocol, name, stype,
            domain, avahi.PROTO_UNSPEC, dbus.UInt32(0),
            reply_handler=service_resolved, error_handler=print_error)

    loop = DBusGMainLoop()

    bus = dbus.SystemBus(mainloop=loop)
    bus = dbus.SystemBus()

    server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
            'org.freedesktop.Avahi.Server')
    server.ResolveService(interface, 0, name, '_presence._tcp', 'local',
                             avahi.PROTO_UNSPEC, dbus.UInt32(0),reply_handler=service_resolved, error_handler=print_error)

    ml = gobject.MainLoop()
    ml.run()

    return ret


def ascii_to_char(match):
    import string
    # replace ascii code with corresponding ASCII character
    return chr(int(match.group(1)))

def list_presence_users(regtype='_presence._tcp', nb_try=10):
    resolved = []
    timeout = 1
    names = {}

    def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                         hosttarget, port, txtRecord):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            tmp = pybonjour.TXTRecord.parse(txtRecord)

            username = fullname.split(".")[0]
            ascii_pattern = re.compile(r"\\(\d\d\d)")
            username = ascii_pattern.sub(ascii_to_char, username)
            ip = resolve(username, interfaceIndex)

            names[username] = {'host': ip,
                               'port': port}
            resolved.append(True)

    def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                        regtype, replyDomain):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return

        if not (flags & pybonjour.kDNSServiceFlagsAdd):
            print 'Service removed'
            return


        resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                    interfaceIndex,
                                                    serviceName,
                                                    regtype,
                                                    replyDomain,
                                                    resolve_callback)

        try:
            while not resolved:
                ready = select.select([resolve_sdRef], [], [], timeout)
                if resolve_sdRef not in ready[0]:
                    print 'Resolve timed out'
                    break
                pybonjour.DNSServiceProcessResult(resolve_sdRef)
            else:
                resolved.pop()
        finally:
            resolve_sdRef.close()


    browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                              callBack = browse_callback)

    try:
        try:
            for i in xrange(nb_try):
                ready = select.select([browse_sdRef], [], [], timeout)
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
        except KeyboardInterrupt:
            pass
    finally:
        browse_sdRef.close()

    return names


def banner_notification(message):
      osso_c = osso.Context("heysms_notif", "0.0.1", False)
      note = osso.SystemNote(osso_c)
      note.system_note_infoprint(message)
