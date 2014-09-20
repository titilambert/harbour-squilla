/*
  Copyright (C) 2013 Jolla Ltd.
                2014 Thibaut Cohen
  Contact: Thibault Cohen <titilambert@gmail.com>
  All rights reserved.

  MainPage.qml

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
import io.thp.pyotherside 1.2


Page {
    id: page

    RemorsePopup {id: delete_popup}

    // To enable PullDownMenu, place our content in a SilicaFlickable
    SilicaFlickable {
        anchors.fill: parent

        // PullDownMenu and PushUpMenu must be declared in SilicaFlickable, SilicaListView or SilicaGridView

        // Tell SilicaFlickable the height of its content.
        contentHeight: column.height

        // Place our content in a Column.  The PageHeader is always placed at the top
        // of the page, followed by our content.
        Column {
            id: column

            anchors.fill: parent

            width: page.width
            spacing: Theme.paddingLarge
            PageHeader {
                title: qsTr("Squilla")
            }

            TextField {
                width: 400
                id: username_field
                placeholderText: "Enter Username"
                label: "Username"


            }

            TextField {
                width: 400
                id: password_field
                placeholderText: "Enter Password"
                echoMode: TextInput.Password
                label: "Password"
            }

           function show_authentication(auth){
                username_field.text = auth.username
                password_field.text = auth.password

           }


           IconTextSwitch {
               id: start_stop_daemon_switch
               text: "Start Squilla Daemon"
               icon.source: "image://theme/icon-m-gps"
               description: "Squilla daemon stopped"
               onCheckedChanged: {
                   py.call("squilla.lib.daemon_manager.start_stop_daemon", [checked])
               }

               function show_daemon_status(state){
                   start_stop_daemon_switch.checked = state
                   if (state == true){
                       start_stop_daemon_switch.description = "Squilla daemon started"
                       start_stop_daemon_switch.text = "Stop Squilla Daemon"
                   }
                   else {
                       start_stop_daemon_switch.description = "Squilla daemon stopped"
                       start_stop_daemon_switch.text = "Start Squilla daemon"
                   }
                
               }
    
           } 

           Label {
                id: interfaces_label
                x: Theme.paddingLarge
               text: "Squilla addresses:"

           }

           TextArea {
               id: interfaces_text
               readOnly: true
               anchors.top: interfaces_label.bottom
               x: Theme.paddingLarge
               focus: false
               text: "Loading..."

               function show_interfaces(interfaces) {
                   var tmp = ''
                   for (var i=0; i<interfaces.length; i++) {
                       if (interfaces[i].ipv4){
                           tmp += interfaces[i].ipv4 + "\n"
                       }
                       if (interfaces[i].ipv6){
                           tmp += interfaces[i].ipv6 + "\n"
                       }
                   }
                   interfaces_text.text = tmp
               }
           } 

           Python {
               id: py
               Component.onCompleted: {
                   // First get data
                   py.call("squilla.lib.config.get_authentication", [], function(auth) {
                       column.show_authentication(auth)
                   })

                   py.call("squilla.lib.daemon_manager.daemon_is_running", [], function(result) {
                       start_stop_daemon_switch.show_daemon_status(result)
                   }) 

                   py.call("squilla.lib.utils.get_urls", [], function(interfaces) {
                       interfaces_text.show_interfaces(interfaces)
                   }) 

                   // Set handlers
                   setHandler('show_authentication', function(auth) {
                       column.show_authentication(auth)
                   })
                   setHandler('show_daemon_status', function(state) {
                       start_stop_daemon_switch.show_daemon_status(state)
                   })

                   setHandler('show_interfaces', function(interfaces) {
                        interfaces_text.show_interfaces(interfaces)
                   })
               }

           }
       }
   }

}


