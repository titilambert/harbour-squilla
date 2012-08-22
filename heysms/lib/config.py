#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    config.py
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


import os
import subprocess
import time

from PyQt4 import QtCore, QtGui

from lib import banner_notification


class Config(QtCore.QSettings):
    def __init__(self, parent=None):
        QtCore.QSettings.__init__(self,
                         '/home/' + os.getenv( 'USER' ) + '/.heysms',
                         0, parent)
        self.parent = parent
        self.last_authorized_bonjour_contact = ""

        # Compatibility mode
        self.use_smssend, _ = self.value("use_smssend").toInt()

        # toggle_profile
        self.manage_profile, _ = self.value("manage_profile").toInt()

        # startup_friends
        raw_friends = self.value("startup_friends")
        self.startup_friends = [str(i.toString()) for i in raw_friends.toList()]

        # start network usb
        self.useusb, _ = self.value("useusb").toInt()

    def update_last_authorized_user(self, contact):
        self.last_authorized_bonjour_contact = contact
        self.setValue("last_authorized_bonjour_contact", QtCore.QVariant(contact))

    def read_last_authorized_bonjour_contact(self):
        raw_contact = self.value("last_authorized_bonjour_contact")
        return str(raw_contact.toString())

    def del_startup_contacts(self, friend):
        self.startup_friends.remove(friend.number)
        self.setValue("startup_friends", QtCore.QVariant(self.startup_friends))

    def add_startup_contacts(self, friend):
        self.startup_friends.append(friend.number)
        self.startup_friends = list(set(self.startup_friends))
        self.setValue("startup_friends", QtCore.QVariant(self.startup_friends))
        self.sync()

    def toggle_smssend(self, state):
        self.setValue("use_smssend", QtCore.QVariant(state))

    def toggle_profile(self, state=None):
        if state is None:
            state = self.manage_profile

        if state == QtCore.Qt.Checked:
            r = os.system('/usr/bin/dbus-send '
                      '--type=method_call '
                      '--dest=com.nokia.profiled '
                      '/com/nokia/profiled '
                      'com.nokia.profiled.set_profile '
                      'string:"silent"')
            self.manage_profile = QtCore.Qt.Checked
        else:
            r = os.system('/usr/bin/dbus-send '
                      '--type=method_call '
                      '--dest=com.nokia.profiled '
                      '/com/nokia/profiled '
                      'com.nokia.profiled.set_profile '
                      'string:"general"')
            self.manage_profile = QtCore.Qt.Unchecked

        self.setValue("manage_profile",
                      QtCore.QVariant(self.manage_profile))
        self.sync()

    def init_profile(self):
        s = subprocess.Popen("/usr/bin/dbus-send "
                             "--type=method_call "
                             "--print-reply "
                             "--dest=com.nokia.profiled "
                             "/com/nokia/profiled "
                             "com.nokia.profiled.get_profile",
                             shell=True, stdout=subprocess.PIPE)
        try:
            p = s.stdout.readlines()[-1].strip()
            self.orig_profile = p.split('"')[1]
        except:
            self.orig_profile = "general"
        if self.manage_profile == QtCore.Qt.Checked:    
            self.toggle_profile()

    def toggle_useusb(self, state):
        # Save parameter
        self.setValue("useusb", QtCore.QVariant(state))

        # Start usb
        if state == QtCore.Qt.Checked:
            # Check current module
            s = subprocess.Popen("cat "
                                 "/proc/driver/musb_hdrc "
                                 "| "
                                 "grep "
                                 '"Gadget driver:" ',
                                 shell=True, stdout=subprocess.PIPE)
            ret = s.stdout.readlines()
            if len(ret) > 0:
                if ret[0].find('g_file_storage') != -1:
                    # Disable g_file_storage module
                    s = subprocess.Popen("echo "
                             "' "
                             "/sbin/rmmod "
                             "g_file_storage "
                             "' "
                             "| "
                             "sudo "
                             "gainroot ",
                             shell=True, stdout=subprocess.PIPE)

                time.sleep(1)
                if ret[0].find('g_ether') != -1 and ret[0].find('(none)') != -1:
                    banner_notification("Please don't set USB mode")
                    return

            # Check if usb0 is used
            if ret[0].find('g_ether') != -1: 
                s = subprocess.Popen("/sbin/ifconfig "
                                     "usb0",
                                     shell=True, stdout=subprocess.PIPE)
                ret = s.stdout.readlines()
                if any([l for l in ret if l.find('addr:') != -1]):
                    # usb already used
                    banner_notification("USB network is currently used ...")
                    return
            time.sleep(1)
            # mount ethernet module
            s = subprocess.Popen("echo "
                                 "' "
                                 "/sbin/modprobe "
                                 "g_ether "
                                 "' "
                                 "| "
                                 "sudo "
                                 "gainroot ",
                                 shell=True, stdout=subprocess.PIPE)
            # Waiting for mount moule
            time.sleep(1)
            # Set IP
            network = "192.168.55."
            s = subprocess.Popen("echo "
                                 "' "
                                 "/sbin/ifconfig "
                                 "usb0 "
                                 + network + "1 "
                                 "netmask "
                                 "255.255.255.0 "
                                 "up "
                                 "' "
                                 "| "
                                 "sudo "
                                 "gainroot ",
                                 shell=True, stdout=subprocess.PIPE)
            time.sleep(1)            
            # launch dhcp server (dnsmasq)
            self.dns_sp = subprocess.Popen("echo "
                                 "' "
                                 "/usr/sbin/dnsmasq "
                                 "--no-daemon "
                                 "-i "
                                 "usb0 "
                                 "-a "
                                 + network + "1 "
                                 "-I "
                                 "lo "
                                 "-z "
                                 "--dhcp-range=" + network + "10," + network + "200,6h "
                                 "--dhcp-authoritative "
                                 "' "
                                 "| "
                                 "sudo "
                                 "gainroot ",
                                 shell=True, stdout=subprocess.PIPE)
        else:
            self.restore_useusb()

    def init_useusb(self):
        self.toggle_useusb(self.useusb)

    def restore_useusb(self):
        s = subprocess.Popen("pgrep "
                             "-lf "
                             "dnsmasq "
                             "| "
                             "grep "
                             '"i usb0" '
                             "| "
                             "cut "
                             "-d "
                             '" " '
                             "-f "
                             "1",
                             shell=True, stdout=subprocess.PIPE)
        for pid in s.stdout.readlines():
            s = subprocess.Popen("echo "
                                 "'"
                                 "kill "
                                 + pid +
                                 "' "
                                 "| "
                                 "sudo "
                                 "gainroot ",
                                 shell=True, stdout=subprocess.PIPE)
        time.sleep(0.5)
        s = subprocess.Popen("echo "
                             "' "
                             "/sbin/ifconfig "
                             "usb0 "
                             "down "
                             "' "
                             "| "
                             "sudo "
                             "gainroot ",
                             shell=True, stdout=subprocess.PIPE)
        s = subprocess.Popen("echo "
                             "' "
                             "/sbin/rmmod "
                             "g_ether "
                             "' "
                             "| "
                             "sudo "
                             "gainroot ",
                             shell=True, stdout=subprocess.PIPE)
        time.sleep(1)
        s = subprocess.Popen("echo "
                             "' "
                             "/sbin/modprobe "
                             "g_file_storage "
                             "' "
                             "| "
                             "sudo "
                             "gainroot ",
                             shell=True, stdout=subprocess.PIPE)



    def restore_profile(self):
        if self.manage_profile == QtCore.Qt.Checked:
            r = os.system('/usr/bin/dbus-send '
                      '--type=method_call '
                      '--dest=com.nokia.profiled '
                      '/com/nokia/profiled '
                      'com.nokia.profiled.set_profile '
                      'string:"%s"' % self.orig_profile)


class Config_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.config = config
        self.silent_label = QtGui.QLabel('Switch in Silent mode when HeySms starts')
        self.silent_checkbox = QtGui.QCheckBox(self)
        self.silent_checkbox.setCheckState(config.manage_profile)
        self.silent_checkbox.setFixedWidth(70)
        self.use_smssend_label = QtGui.QLabel('Use Smssend to send Sms')
        self.smssend_checkbox = QtGui.QCheckBox(self)
        self.smssend_checkbox.setCheckState(config.use_smssend)
        self.smssend_checkbox.setFixedWidth(70)
        self.useusb_label = QtGui.QLabel('Activate USB networking')
        self.useusb_checkbox = QtGui.QCheckBox(self)
        self.useusb_checkbox.setCheckState(config.useusb)
        self.useusb_checkbox.setFixedWidth(70)
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.silent_label, 0, 0)
        mainLayout.addWidget(self.silent_checkbox, 0, 1)
        mainLayout.addWidget(self.use_smssend_label, 1, 0)
        mainLayout.addWidget(self.smssend_checkbox, 1, 1)
        mainLayout.addWidget(self.useusb_label, 2, 0)
        mainLayout.addWidget(self.useusb_checkbox, 2, 1)
        mainLayout.setRowStretch(0, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle('Preferences')

        QtCore.QObject.connect(self.silent_checkbox,
                               QtCore.SIGNAL("stateChanged(int)"),
                               self.toggle_profile)
        QtCore.QObject.connect(self.smssend_checkbox,
                               QtCore.SIGNAL("stateChanged(int)"),
                               self.toggle_smssend)
        QtCore.QObject.connect(self.useusb_checkbox,
                               QtCore.SIGNAL("stateChanged(int)"),
                               self.toggle_useusb)

    def toggle_useusb(self, state):
        config.toggle_useusb(state)

    def toggle_profile(self, state):
        config.toggle_profile(state)

    def toggle_smssend(self, state):
        s = subprocess.Popen("/usr/bin/which "
                             "smssend ",
                             shell=True, stdout=subprocess.PIPE)
        res = s.stdout.readlines()
        smssend_installed = False 
        if len(res) == 1:
            smssend_installed = True 

        if not smssend_installed:
            banner_notification("You need to install smssend")
            QtCore.QObject.disconnect(self.smssend_checkbox,
                               QtCore.SIGNAL("stateChanged(int)"),
                               self.toggle_smssend)
            self.smssend_checkbox.setCheckState(QtCore.Qt.Unchecked)
            QtCore.QObject.connect(self.smssend_checkbox,
                               QtCore.SIGNAL("stateChanged(int)"),
                               self.toggle_smssend)
            return

        state = self.smssend_checkbox.checkState()
        config.toggle_smssend(state)
    

config = Config()
