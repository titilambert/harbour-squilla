#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    heysms.py
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


import sys
import os
from datetime import datetime
from time import sleep
from optparse import OptionParser

from PyQt4 import QtCore, QtGui
try:
    import osso
except:
    pass

from lib.lib import banner_notification, list_presence_users
from lib.server import Bonjour_server
from lib.sms_listener import Sms_listener
from lib.scheduler import Scheduler
from lib.lib import logger
from lib.friend import Friend
from lib.config import config, Config_dialog
from lib.friend_list import Friend_list_widget


class MenuBar(QtGui.QMenuBar):
    def __init__(self, parent=None, ):
        QtGui.QMenuBar.__init__(self, parent)
        self.setObjectName("Menu")
        self.preference = self.addAction(self.tr("&Preferences"))
        ## Quit
        self.quit = self.addAction(self.tr("&Quit"))


class Central_widget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent

        # Load gui items
        self.bonjour_users_label = QtGui.QLabel('Select your Bonjour '
                                                'contact id :')
        self.bonjour_users_label.setFixedHeight(50)
        self.bonjour_users = QtGui.QComboBox()
        icon = QtGui.QIcon('/usr/share/icons/hicolor/48x48/hildon'
                           '/general_refresh.png')
        self.reload_bonjour_users_button = QtGui.QPushButton()
        self.reload_bonjour_users_button.setIcon(icon)
        self.reload_bonjour_users_button.setFixedWidth(80)
        self.empty = QtGui.QLabel('')
        self.friend_list_label = QtGui.QLabel('Friends list :')
        self.friends_list = Friend_list_widget(self)
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.bonjour_users_label, 0, 0, 1, 2)
        mainLayout.addWidget(self.bonjour_users, 1, 0)
        mainLayout.addWidget(self.reload_bonjour_users_button, 1, 1)
        
        mainLayout.addWidget(self.empty, 4, 0, 1, 2)
        mainLayout.addWidget(self.friend_list_label, 5, 0, 1, 2)
        mainLayout.addWidget(self.friends_list, 6, 0, 1, 2)

        mainLayout.setRowStretch(0, 0)
        self.setLayout(mainLayout)

    def reload_contacts(self):
        self.parent.main_window.setAttribute(
                                    QtCore.Qt.WA_Maemo5ShowProgressIndicator,
                                    True)
        self.parent.main_window.repaint()
        banner_notification("Looking for Bonjour contacts ...")
        self.parent.bonjour_users = list_presence_users()
        self.bonjour_users.clear()
        if len(self.parent.bonjour_users) == 0:
            banner_notification("No Bonjour contacts found !")
        else:
            node_friend_list = [f.node for f in 
                                self.parent.scheduler.friend_list]
            for bonjour_user, info in self.parent.bonjour_users.items():
                # if the contact was create by heysms
                # we don't want to see it in the list
                if bonjour_user in node_friend_list:
                        continue
                self.bonjour_users.addItem(bonjour_user)
            # Read last bonjour_contact used
            last_authorized_bonjour_contact = config.read_last_authorized_bonjour_contact()
            # Search in list last bonjour_contact used
            index = self.bonjour_users.findText(last_authorized_bonjour_contact)
            if index != -1:
                # Select last bonjour_contact used
                logger.debug("Last Bonjour contact found: %s, we select it" % last_authorized_bonjour_contact)
                self.bonjour_users.setCurrentIndex(index)

            self.parent.change_bonjour_user(self.bonjour_users.currentText())
            banner_notification("Bonjour contacts loaded !")

        self.parent.main_window.setAttribute(
                                    QtCore.Qt.WA_Maemo5ShowProgressIndicator,
                                    False)


class Ui_MainWindow(QtCore.QObject):
    def __init__(self, app):
        QtCore.QObject.__init__(self)
        self.app = app
        self.friend_list = []
        self.bonjour_auth_user = ''
        self.bonjour_users = {}

    def setupUi(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(800, 400)

        self.central_widget = Central_widget(self)
        self.main_window.setCentralWidget(self.central_widget)
        self.main_window.conf_dialog = Config_dialog(self.main_window)
        # Set ui
        config.init_profile()

        ### Menu
        self.menubar = MenuBar(self.main_window)
        self.main_window.setMenuBar(self.menubar)

        QtCore.QMetaObject.connectSlotsByName(self.main_window)

        # Signals
        QtCore.QObject.connect(self.central_widget.reload_bonjour_users_button,
                               QtCore.SIGNAL("pressed ()"),
                               self.central_widget.reload_contacts)
        QtCore.QObject.connect(self.central_widget.bonjour_users,
                               QtCore.SIGNAL("currentIndexChanged "
                                             "(const QString&)"),
                               self.change_bonjour_user)

        QtCore.QObject.connect(self.menubar.preference,
                               QtCore.SIGNAL("triggered()"),
                               self.main_window.conf_dialog.exec_)
        ## Quit
        QtCore.QObject.connect(self.menubar.quit,
                               QtCore.SIGNAL("triggered()"),
                               self.app.quit)

    def toggle_server(self):
        if not hasattr(self, 'bs'):
            self.bonjour_auth_user = self.central_widget.bonjour_users\
                                         .currentText()
            self.bs = Bonjour_server(self.bonjour_auth_user)
        if self.bs.is_running():
            pass
#            self.bs.stop()
        else:
            self.bs.listen()

    def change_bonjour_user(self, new_bonjour_user):
        if not hasattr(self, 'bs'):
            self.toggle_server()
        else:
            self.bs.set_auth(new_bonjour_user)
            self.bonjour_auth_user = new_bonjour_user
            self.scheduler.set_auth(new_bonjour_user)
            config.update_last_authorized_user(new_bonjour_user)


def main():

    def exit():
        logger.debug("Stopping active friends")
        for f in ui.friend_list:
            f.close()
        logger.debug("Restore profile")
        config.restore_profile()

    opt_parser = OptionParser()
    opt_parser.add_option("-d", "--debug", dest="debug_mode",
                          action="store_true",
                          default='False', help="Debug mode")

    app = QtGui.QApplication(sys.argv)
#    app.setOrganizationName("HeySms")
#    app.setOrganizationDomain("HeySms")
    app.setApplicationName("HeySms")
    (options, args) = opt_parser.parse_args([str(i) for i in app.arguments()])
    logger.set_debug(options.debug_mode)
    
    main_window = QtGui.QMainWindow()
    ui = Ui_MainWindow(app)
    ui.setupUi(main_window)
    config.parent = ui

    ui.sms_listener = Sms_listener(ui)
    ui.sms_listener.start()
    logger.debug("Sms_listener started")
    ui.scheduler = Scheduler(ui)
    ui.scheduler.start()
    logger.debug("Scheduler started")

    main_window.setWindowTitle("HeySms")
    main_window.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
    main_window.show()
    main_window.repaint()
    ui.central_widget.repaint()
    ui.central_widget.reload_contacts()


    QtCore.QObject.connect(app,
                           QtCore.SIGNAL("lastWindowClosed()"),
                           exit)

    sys.exit(app.exec_())


    
