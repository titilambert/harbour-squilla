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
    id: friendslistpage

    RemorsePopup {id: add_friend_popup}

    Component {
        id: friend_delegate

        ListItem {
            width: 480
            height: 80

            onClicked: {
                add_friend_popup.execute("Add friend: " + name, function () {
                    py.call("squilla.lib.add_friend", [name, number])
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





