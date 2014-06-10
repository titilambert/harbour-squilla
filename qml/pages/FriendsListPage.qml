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
//import QtContacts 5.0
import org.nemomobile.contacts 1.0


Page {
    id: friendslistpage

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


    PageHeader {
        id: pageheader
        title: qsTr("Add friend")
    }

    SilicaListView {
        id: friend_list
        anchors.fill: parent
        anchors.topMargin: 100
        width: 480
        height: 100


        header: SearchField {
            id: searchField
            width: parent.width
            placeholderText: "Search"

            onTextChanged: {
                peopleModel.search(searchField.text)
            }
        }

        //model: ContactModel {}
        model: PeopleModel {
                id: peopleModel
            }

        delegate: Text {
            text: "Name: " + model.contact.name.firstName + " " + model.contact.name.lastName + " Number: " + model.contact.phoneNumber.number

        }
/*
        model: ListModel {
            id: listModel

            function search(text) {
                py.call("friend_list.get_data", [text], function(result) {
                            // Load the received data into the list model
                            for (var i=0; i<result.length; i++) {
                                listModel.append(result[i]);
                            }
                        });
            }


        }


        // prevent newly added list delegates from stealing focus away from the search field
        currentIndex: -1



        delegate: friend_delegate
*/
    }


    Python {
        id: py

        Component.onCompleted: {
            // Add the directory of this .qml file to the search path
            addImportPath(Qt.resolvedUrl('.'));

            // Import the main module and load the data
            importModule('friend_list', function () {
                        py.call('friend_list.get_data', [], function(result) {
                            // Load the received data into the list model
                            for (var i=0; i<result.length; i++) {
                                listModel.append(result[i]);
                            }
                        });
            });
        }
    }

}





