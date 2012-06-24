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

from PyQt4 import QtCore, QtGui


class Config(QtCore.QSettings):
    def __init__(self, parent=None):
        QtCore.QSettings.__init__(self,
                         '/home/' + os.getenv( 'USER' ) + '/.heysms',
                         0, parent)
        self.parent = parent
        self.compatibility_mode = ""
        self.last_authorized_bonjour_contact = ""

        # toggle_profile
        self.manage_profile, _ = self.value("manage_profile").toInt()

        # startup_friends
        raw_friends = self.value("startup_friends")
        self.startup_friends = [str(i.toString()) for i in raw_friends.toList()]

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
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.silent_label, 0, 0)
        mainLayout.addWidget(self.silent_checkbox, 0, 1)
        mainLayout.setRowStretch(0, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle('Preferences')

        QtCore.QObject.connect(self.silent_checkbox,
                               QtCore.SIGNAL("stateChanged(int)"),
                               self.toggle_profile)

    def toggle_profile(self, state):
        config.toggle_profile(state)
    

config = Config()

