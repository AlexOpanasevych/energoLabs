import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.0
import QtQuick.Dialogs 1.2

Window {
    visible: true
    width: 1280
    height: 720
    title: qsTr("Gzafsgs")

    TabView {
        anchors.fill: parent
        Tab {
        }
        Tab {

            ColumnLayout {
                RowLayout {
                    height: 50
                    Layout.fillWidth: parent.width
                    Button {
                        text: "add user"
                        height: 50
                        width : 80
                        onClicked: {
                            inputDialog.userIndex = userMenu.userIndex
                            inputDialog.editMode = 1
                            inputDialog.open()
                        }
                    }
                    Item {
                        Layout.fillWidth: true
                    }
                }



                ListView {

                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    model: shitModel

                    spacing: 4

                    delegate: Rectangle {
                        height: 50
                        width: parent !== null ? parent.width : 0
                        User {
                            name: name
                            lastname: lastName
                        }

                        RowLayout {
                            anchors.fill: parent
                            Text {
                                Layout.fillHeight: true
                                text: name + " " + lastName
                                font.pixelSize: 50 / 3
                            }
                            // and so on
                        }

                        MouseArea {
                            anchors.fill: parent
                            acceptedButtons: Qt.RightButton

                            onClicked: {
                                userMenu.userIndex = index
                                userMenu.popup()
                            }
                        }

                    }



                }


            }

        }
        Tab {}
        Tab {}
    }

    Dialog {
        id: inputDialog
        standardButtons: StandardButton.Ok | StandardButton.Cansel
        title: "Введіть дані користувача"
        property string lastInputName
        property string lastInputLastName

        property int userIndex

        property int editMode

        ColumnLayout {
            Label {text: "Ім'я"}
            TextField {
                validator: RegExpValidator {
                    regExp: /[a-zA-Z]+/
                }
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.lastInputName = text
                    }
                }
            }
            Label {text: "Прізвище"}
            TextField {
                validator: RegExpValidator {
                    regExp: /[a-zA-Z]+/
                }
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.lastInputLastName = text
                    }
                }
            }
        }
        onAccepted: {
//            for(let i = 0; i < shitModel.count; i++) {
//                if(shitModel.get(index).name == lastInputName )
//            }
            switch(editMode) {
            case 1:
                shitModel.append({"name": lastInputName, "lastName": lastInputLastName})
                break
            case 2:
                shitModel.get(userIndex).name = lastInputName
                shitModel.get(userIndex).lastName = lastInputLastName
                break
            }

        }
    }

    Menu {
        id: userMenu
        property int userIndex
        MenuItem {
            text: "remove user"
            onTriggered: {
                shitModel.remove(userMenu.userIndex)
            }
        }
        MenuItem {
            text: "update info"
            onTriggered: {
                inputDialog.editMode = 2
                inputDialog.open()
            }
        }
    }

    Dialog {

    }

    ListModel {
        id: shitModel
    }

}
