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

    onStatusChanged: {
                      if (status == 2) {
                        presence_combo.reload()
                      }
                     }

    // To enable PullDownMenu, place our content in a SilicaFlickable
    SilicaFlickable {
        anchors.fill: parent

        // PullDownMenu and PushUpMenu must be declared in SilicaFlickable, SilicaListView or SilicaGridView
        PullDownMenu {
            MenuItem {
                text: qsTr("Preferences")
                onClicked: pageStack.push(Qt.resolvedUrl("PreferencesPage.qml"))
            }
            MenuItem {
                text: qsTr("Add friend")
                onClicked: pageStack.push(Qt.resolvedUrl("FriendsListPage.qml"))
            }
        }

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

            ComboBox {
                width: 480
                id: presence_combo
                label: "Select your Bonjour contact ID"


                menu: ContextMenu {
                    id: presence_contextmenu
                    Repeater { 
                        id: presence_repeater_combo
                        model: ListModel { id: presence_model }
                        MenuItem { text: model.name }
                    }
                }

                function reload(selected_presence) {
                    //Get uccrent selected name
                   // current_selected = presence_model.get(presence_combo.currentIndex).name
                    // Clear list
                    presence_model.clear()
                    py.call('squilla.lib.presence_browser.load_presences', [selected_presence], function(result) {
                            for (var i=0; i<result.length; i++) {
                                presence_model.append(result[i])
                            }
                    })
                    // Find old selected name in the new list
//                    current_selected
                    // Select the old selected name in combo box

                    // Update selected user if old name is not found

                }

                onClicked: {
                    presence_combo.reload()
                    if (presence_combo.currentItem != null) {
                        if (presence_combo.currentItem.text != ''){
                            py.call('squilla.lib.set_presence_auth_user', [presence_model.get(presence_combo.currentIndex).text]);
                        }
                    }
                }

                onCurrentIndexChanged: {
                    if (presence_combo.currentItem != null) {
                        if (presence_combo.currentItem.name != ''){
                            py.call('squilla.lib.set_presence_auth_user', [presence_model.get(presence_combo.currentIndex).name]);
                        }
                    }
                }
            }

            Label {
                x: Theme.paddingLarge
                text: qsTr("Friends list:")
                color: Theme.secondaryHighlightColor
                font.pixelSize: Theme.fontSizeExtraLarge
                height: 60
            }

            Component {
                id: active_friend_delegate
                Item {
                    width: 480
                    height: 80
                    id: friend_listitem

                    Column {
                        id: friend_row

                        Text { 
                            id: friend_name
                            text: name
                            color: Theme.primaryColor
                            width: 360
                            anchors.leftMargin: 20
                        //    anchors.top: parent.top
                            anchors.left: parent.left

                            IconButton {
                                icon.source: 'image://theme/icon-m-favorite' + (favorite ? '-selected' : '')
                                id: friend_fav
                                anchors.left: parent.right
                                height: 30
                                onClicked: {
                                        py.call("squilla.lib.config.set_favorite", [number, name], function(result) {
                                            if (result == true) {
                                                icon.source = 'image://theme/icon-m-favorite-selected'
                                            }
                                            else {
                                                icon.source = 'image://theme/icon-m-favorite'
                                            }
                                        })
                                }
                                IconButton {
                                    icon.source: 'image://theme/icon-m-delete'
                                    anchors.left: parent.right
                                    anchors.top: parent.top
                                    anchors.verticalCenter: parent.verticalCenter
                                    onClicked: {
                                                delete_popup.execute("Deleting", function () {
                                                    py.call("squilla.lib.friend.delete_friend", [number], function(result) {
                                                         if (result != null) {
                                                                listModel2.remove(result, 1)
                                                         }
                                                    })
                                                })
                                    }
                                }
                            }
                        }
                    }

                }
            }

            SilicaListView {
                id: active_friend_list
                width: 480
                height: 800
                model: ListModel {
                    id: listModel2
                }
                delegate: active_friend_delegate
            }

            Python {
                id: py
                Component.onCompleted: {
                    setHandler('add_friend_list', function(friend) {
                        listModel2.append(friend);
                    })
                    setHandler('set_selected_auth_user', function(auth_user) {
                        presence_combo.reload(auth_user);
                    })
                }

            }


        }
    }

}


