/*
  Copyright (C) 2013 Jolla Ltd.
  Contact: Thomas Perl <thomas.perl@jollamobile.com>
  All rights reserved.

  You may use this file under the terms of BSD license as follows:

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Jolla Ltd nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR
  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.2


Page {
    id: page

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
                title: qsTr("HeySMS")
            }

            ComboBox {
                width: 480
                id: contactComboBox
                label: "Select your Bonjour contact ID"

                menu: ContextMenu {
                    MenuItem { text: "automatic" }
                    MenuItem { text: "manual" }
                    MenuItem { text: "high" }
                }
            }
            Label {
                x: Theme.paddingLarge
                id: toto
                text: qsTr("Friends list:")
                color: Theme.secondaryHighlightColor
                font.pixelSize: Theme.fontSizeExtraLarge
            }

            Component {
                id: friend_delegate
                Item {
                    width: 480
                    height: 60

                    Column {
                        id: friend_row
                        anchors.leftMargin: 20
                        anchors.fill: parent
                        anchors.top: parent.top

                        Text { 
                            id: friend_name
                            text: name
                            //anchors.horizontalCenter: parent.horizontalLeft;
                            color: team
                            width: 380

                            Text {
                                text: "FAV";
                                id: friend_fav
                                width: 60
                                anchors.left: parent.right
                                anchors.top: parent.top
        
                                Text {
                                    text: "DEL";
                                    width: 60
                                    anchors.left: parent.right
                                    anchors.top: parent.top
                                }
                            }
                        }
                 //     Image { source: portrait; anchors.horizontalCenter: parent.horizontalCenter }
                    }
                }
            }

            SilicaListView {
                id: friend_list
                width: 480
                height: 800
                model: ListModel {
                    id: listModel2
                }
                delegate: friend_delegate
            }

            Python {
                id: py

                Component.onCompleted: {
                    // Add the directory of this .qml file to the search path
                    addImportPath(Qt.resolvedUrl('../../heysms'));

                    // Import the main module and load the data
                    importModule('friend_list', function () {
                        py.call('friend_list.get_data', [], function(result) {
                            // Load the received data into the list model
                            for (var i=0; i<result.length; i++) {
                                listModel2.append(result[i]);
                            }
                        });
                    });
                }
            }


        }
    }

}


