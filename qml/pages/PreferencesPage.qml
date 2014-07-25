/*
  Copyright (C) 2013 Jolla Ltd.
                2014 Thibaut Cohen
  Contact: Thibault Cohen <titilambert@gmail.com>
  All rights reserved.

  PreferencesPage.qml

  This file is part of Squilla

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

import QtQuick 2.0
import Sailfish.Silica 1.0


Page {
    id: page

    SilicaFlickable {
        anchors.fill: parent

        // Tell SilicaFlickable the height of its content.
        contentHeight: column.height

        Column {
            id: column

            width: page.width
            spacing: Theme.paddingLarge
            PageHeader {
                title: qsTr("Preferences")
            }

            TextSwitch {
                id: silentSwitch
                text: "Switch to Silent mode when Squilla starts"
                onClicked: {
                    py.call('squilla.lib.config.set_silent_mode', [checked])
                }
                Component.onCompleted: {
                    py.call('squilla.lib.config.get_silent_mode', [], function(result) {
                        if (result == true) {
                            silentSwitch.checked = true
                        }
                    })
                }
            }

            TextSwitch {
                id: usbSwitch
                text: "Activate USB networking (NOT WORKING)"
                /*description: "Activates the Doomsday device"
                /*onCheckedChanged: {
                    device.setStatus(checked ? DeviceState.Armed : DeviceState.Disarmed)
                }*/
            }

            TextSwitch {
                id: controllerSwitch
                text: "Active Controller Contact (NOT WORKING)"
                /*description: "Activates the Doomsday device"
                /*onCheckedChanged: {
                    device.setStatus(checked ? DeviceState.Armed : DeviceState.Disarmed)
                }*/
            }
        }
    }
}
