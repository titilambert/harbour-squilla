/*
  Copyright (C) 2013 Jolla Ltd.
                2014 Thibaut Cohen
  Contact: Thibault Cohen <titilambert@gmail.com>
  All rights reserved.

  FriendsListPage.qml

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
    id: friendslistpage

    RemorsePopup {id: add_friend_popup}

    Component {
        id: friend_delegate

        ListItem {
            width: 480
            height: 80

            onClicked: {
                add_friend_popup.execute("Add friend: " + name, function () {
                    py.call("squilla.lib.friend.add_friend", [name, number])
                    pageStack.pop()
                }, 2000)
            }

            Column {
                id: friend_row
                anchors.leftMargin: 20
                anchors.fill: parent
                anchors.top: parent.top

                Text {
                    id: friend_name
                    text: name
                    color: Theme.primaryColor
                    height: 40
                    width: 480


                    Text {
                        id: friend_fav
                        font.pixelSize: Theme.fontSizeExtraSmall
                        height: 20
                        width: 480
                        text: number
                        color: Theme.primaryColor
                        anchors.left: parent.left
                        anchors.top: parent.bottom

                    }
                }
            }
        }
    }


    PageHeader {
        id: pageheader
        title: qsTr("Add friend")
    }

    SilicaListView {
        id: friend_list
        anchors.fill: parent
        anchors.topMargin: 100
        currentIndex: -1
        width: 480
        height: 100

        header: SearchField {
            id: searchField
            width: parent.width
            placeholderText: "Search"
            focus: true

            onTextChanged: {
                peopleModel.update(searchField)
            }
        }

        model: ListModel {
                id: peopleModel

                function update(searchField) {
                    clear()
                    py.call('squilla.lib.list_contact', [searchField.text], function(result) {
                            // Load the received data into the list model
                            for (var i=0; i<result.length; i++) {
                                peopleModel.append(result[i]);
                            }
                    });
                }
        }

        delegate: friend_delegate
    }

    Python {
        id: py

        Component.onCompleted: {
            importModule('squilla', function () {
                        py.call('squilla.lib.list_contact', [], function(result) {
                            // Load the received data into the list model
                            for (var i=0; i<result.length; i++) {
                                peopleModel.append(result[i]);
                            }
                        });
            });

        }
    }

}





