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

from PyQt4 import QtCore, QtGui
try:
    import osso
except:
    pass

from lib.lib import *
from lib.server import *
from lib.sms_listener import *
from lib.friend import *
from lib.scheduler import *


class MenuBar(QtGui.QMenuBar):
    def __init__(self, parent=None, ):
        QtGui.QMenuBar.__init__(self, parent)
        self.setObjectName("Menu")
        ## Quit
        self.quit = self.addAction(self.tr("&Quit"))


class Central_widget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.parent = parent

        # Load gui items
        self.bonjour_users_label = QtGui.QLabel('Select your Bonjour '
                                                'contact id :')
        self.empty = QtGui.QLabel('')
        self.bonjour_users_label.setFixedHeight(50)
        self.bonjour_users = QtGui.QComboBox()
        self.start_server_button = QtGui.QPushButton('Start server')
        icon = QtGui.QIcon('/usr/share/icons/hicolor/48x48/hildon'
                           '/general_refresh.png')
        self.reload_bonjour_users_button = QtGui.QPushButton()
        self.reload_bonjour_users_button.setIcon(icon)
        self.reload_bonjour_users_button.setFixedWidth(80)
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.bonjour_users_label, 0, 0, 2, 1)
        mainLayout.addWidget(self.bonjour_users, 1, 0)
        mainLayout.addWidget(self.reload_bonjour_users_button, 1, 1)
        mainLayout.addWidget(self.empty, 2, 0, 2, 1)
#        mainLayout.addWidget(self.start_server_button, 2, 0)

        mainLayout.setRowStretch(0, 0)
        self.setLayout(mainLayout)

    def reload_contacts(self):
        self.parent.main_window.setAttribute(
                                    QtCore.Qt.WA_Maemo5ShowProgressIndicator,
                                    True)
        self.parent.main_window.repaint()
        banner_notification("Loading Bonjour contacts ...")
        self.parent.bonjour_users = list_presence_users()
        self.bonjour_users.clear()
        if len(self.parent.bonjour_users) == 0:
            banner_notification("NO Bonjour contacts found !")
        else:
            for bonjour_user, info in self.parent.bonjour_users.items():
                self.bonjour_users.addItem(bonjour_user)
            self.parent.bonjour_auth_user = self.bonjour_users.currentText()
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
        #self.config = config.Config(parent=self)

    def setupUi(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(800, 400)

        self.central_widget = Central_widget(self)
        self.main_window.setCentralWidget(self.central_widget)

        ### Menu
        self.menubar = MenuBar(self.main_window)
        self.main_window.setMenuBar(self.menubar)

        QtCore.QMetaObject.connectSlotsByName(self.main_window)

        # Signals
        QtCore.QObject.connect(self.central_widget.reload_bonjour_users_button,
                               QtCore.SIGNAL("pressed ()"),
                               self.central_widget.reload_contacts)
        QtCore.QObject.connect(self.central_widget.start_server_button,
                               QtCore.SIGNAL("pressed ()"),
                               self.toggle_server)
        QtCore.QObject.connect(self.central_widget.bonjour_users,
                               QtCore.SIGNAL("currentIndexChanged "
                                             "(const QString&)"),
                               self.change_bonjour_user)
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
            self.bs.stop()
            self.central_widget.start_server_button.setText("Start Server")
        else:
            self.central_widget.start_server_button.setText("Stop Server")
            self.bs.listen()

    def change_bonjour_user(self, new_bonjour_user):
        if not hasattr(self, 'bs'):
            self.toggle_server()
        else:
            self.bs.set_auth(new_bonjour_user)
            self.bonjour_auth_user = new_bonjour_user
            self.scheduler.set_auth(new_bonjour_user)


def main():
    app = QtGui.QApplication(sys.argv)
#    app.setOrganizationName("HeySms")
#    app.setOrganizationDomain("HeySms")
    app.setApplicationName("HeySms")
    main_window = QtGui.QMainWindow()
    ui = Ui_MainWindow(app)
    ui.setupUi(main_window)

    ui.sms_listener = Sms_listener(ui)
    ui.sms_listener.start()
    ui.scheduler = Scheduler(ui)
    ui.scheduler.start()

    main_window.setWindowTitle("HeySms")
    main_window.setAttribute(QtCore.Qt.WA_Maemo5AutoOrientation, True)
#    main_window.setAttribute(QtCore.Qt.WA_Maemo5StackedWindow, True)
# QtCore.Qt.WA_Maemo5NonComposited
# QtCore.Qt.WA_Maemo5ShowProgressIndicator
# QtCore.Qt.WA_Maemo5LandscapeOrientation
# QtCore.Qt.WA_Maemo5PortraitOrientation
# QtCore.Qt.WA_Maemo5StackedWindow
    main_window.show()
    main_window.repaint()
    ui.central_widget.repaint()
    ui.central_widget.reload_contacts()

    sys.exit(app.exec_())
