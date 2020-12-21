import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import QtWebEngine 1.10

import QtQuick 2.12
import QtQuick.Dialogs 1.2
import QtCharts 2.3

Item {
    id: root
    width: 1280
    height: 720

    TabView {
        anchors.fill: parent

        Tab {
            title: "Аналіз метеорологічних даних регіону | Теплотехнічні характеристики будівлі, потреба у тепловій енергії на опалення, ГВП та вентилювання"
            TabView {

                Tab {

                    WebEngineView {
                        anchors.fill: parent
                        url: "http://127.0.0.1:" + 8090
                    }
                }

                Tab {
                    title: "Звіт 1"
                    ScrollView
                    {
//                        contentWidth: column.width    // The important part
//                        contentHeight: column.height  // Same
                        clip : true

                        Column {
                            width: parent.width
                            Repeater {
                                model: 5;
                                delegate: Item {
                                    width: root.width;
                                    height: image.sourceSize.height;

                                    Image {
                                        id: image;
                                        anchors.centerIn: parent;
                                        width: parent.width;
                                        fillMode: Image.Stretch;
                                        source: "images/first_lab/" + (index+1) + ".jpg"
                                    }
                                }
                            }
                        }
                    }
                }

            }


        }

        Tab {
            title: "Моделювання графіка електричного навантаження"
            TabView {
                Tab {
                    title: "Завдання 1, 2"
                    ColumnLayout {
                        anchors.topMargin: 50
                        anchors.leftMargin: 50
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

                            model: elecModel

                            spacing: 4

                            delegate: Rectangle {
                                height: 50
                                width: parent !== null ? parent.width : 0
                                User {
                                    name: name
                                    power: power
                                }

                                RowLayout {
                                    anchors.fill: parent
                                    Text {
                                        Layout.fillHeight: true
                                        text: name + " Потужність: " + power
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

                            Component.onCompleted: {
                                console.log(elecModel.rowCount())
                            }

                        }


                    }

                }

                Tab {
                    title: "Завдання 3"
                    ChartView {
                        anchors.fill: parent
                        antialiasing: true
                        title: "Графік забезпечення потреб"

                        LineSeries {
                            id: needsGraph
                            axisX: DateTimeAxis {
                                id: dateTimeAxisX
                                titleText: "ЧАС"
                                titleFont.pointSize: 12
                                format: "ddd MMMM d yy"
                                min : new Date(2020, 12, 12)
                                max: new Date(2020, 12, 19)
                            }
                            axisY: ValueAxis {
                                id: yAxis
                                titleText: "КІЛЬКІСТЬ ВИТРАЧЕНОЇ ЕНЕРГІЇ"
                                titleFont.pointSize: 12
                                min: 0
                                max: 1000
                            }
                            name: "Витрачена енергія"
                            XYPoint {x: 2; y: 10}
                            XYPoint {x: 4; y: 10}
                            XYPoint {x: 6; y: 10}
                            XYPoint {x: 8; y: 10}
                            XYPoint {x: 10; y: 10}
                        }
                    }
                }

                Tab {
                    title: "Завдання 4"
                    ChartView {
                        anchors.fill: parent
                        antialiasing: true
                        title: "Графік забезпечення потреб"
                        LineSeries {
                            id: genGraph
                            axisX: DateTimeAxis {
                                id: aX
                                titleText: "ЧАС"
                                titleFont.pointSize: 12
                                format: "ddd MMMM d yyyy"
                                min : new Date(2020, 11, 12)
                                max: new Date(2020, 11, 19)
                            }
                            axisY: ValueAxis {
                                id: aY
                                titleText: "КІЛЬКІСТЬ ВИТРАЧЕНОЇ ЕНЕРГІЇ"
                                titleFont.pointSize: 12
                                min: 0
                                max: 1000
                            }
                            name: "Витрачена енергія"
//                            XYPoint {x: 2; y: 10}
//                            XYPoint {x: 4; y: 10}
//                            XYPoint {x: 6; y: 10}
//                            XYPoint {x: 8; y: 10}
//                            XYPoint {x: 10; y: 10}
                        }
                    }
                }

                Tab {
                    title: "Завдання 5"
                    Item {
                        anchors.margins: 5
                        ComboBox {
                            id: userChoose
                            model: 10
                        }

                        Loader {

                            anchors.top: userChoose.bottom
                            sourceComponent: editComponents
                            onLoaded: {
                                item.init(userChoose.currentText)
                            }
                        }

                        Component {
                            id: editComponents
                            ColumnLayout {
                                Label {text: "W_(спож.)"}
                                TextField {text: "computed value"; readOnly: true}
                                Label {text: "P_(сер.)"}
                                TextField {readOnly: true}
                                Label {text: "T_max"}
                                TextField {readOnly: true}
                                Label {text: "k_(зап.)"}
                                TextField {readOnly: true}
                                Label {text: "k_(вик.)"}
                                TextField {readOnly: true}

                                function init() {
                                    // here will be db select or idk
                                }
                            }


                        }

                    }
                }

                Tab {
                    title: "Завдання 6"
                    ColumnLayout {
                        Text {

                            text: qsTr("Обсяги фінансових витрат за умови використання однозонного тарифу:")
                        }
                        Text {

                            text: qsTr("Обсяги фінансових витрат за умови використання двозонного тарифу:")
                        }
                        Text {

                            text: qsTr("Обсяги фінансових витрат за умови використання тризонного тарифу:")
                        }
                    }
                }

                Tab {
                    title: "Завдання 7"
                }

            }


        }
        Tab {
            title: "Визначення ефективності впровадження вітроенергетичної установки для потреб енергозабезпечення об’єкта"
            TabView {
                Tab {
                    title: "Вкладка вводу"
                    ColumnLayout {
                        anchors.topMargin: 50
                        anchors.leftMargin: 50
                        RowLayout {
                            height: 50
                            Layout.fillWidth: parent.width
                            Button {
                                text: "Додати ВЕУ"
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

                            model: evuModel

                            spacing: 4

                            delegate: Rectangle {
                                height: 50
                                width: parent !== null ? parent.width : 0
                                User {
                                    name: name
                                    power: power
                                }

                                RowLayout {
                                    anchors.fill: parent
                                    Text {
                                        Layout.fillHeight: true
                                        text: name + " Потужність: " + power
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

                Tab {
                    ColumnLayout {
                        Label {text: "V_шукана"}
                        TextField {readOnly: true}
                        Label {text: "Р_ВЕУ"}
                        TextField {readOnly: true}
                        Label {text: "Обсяги генерування електричної енергії за " + "here will be time"}
                        TextField {readOnly: true}
                        Label {text: "т. СО2 екв."}
                        TextField {readOnly: true}
                        Label {text: "Дохід"}
                        TextField {readOnly: true}
                        Label {text: "Ціна на ОСВ"}
                        TextField {readOnly: true}
                    }
                }
                Tab {}
                Tab {}
            }
        }
        Tab {
            title: "Визначення ефективності впровадження вітроенергетичної установки для потреб енергозабезпечення об’єкта"
        }
        Tab {
            title: "Визначення ефективності впровадження повітряного теплового насосу для потреб систем опалення та кондиціонування об’єкта"
        }
    }

    Dialog {
        id: inputDialog
        standardButtons: StandardButton.Ok | StandardButton.Cansel
        title: "Введіть дані користувача"
        property string lastInputName
        property double power
        property double time_of_work
        property int quantity
        property int project_id
        property int switch_off_id
        property int switch_on_id
        property int userIndex

        property int editMode

        ColumnLayout {
            Label {text: "Ім'я"}
            TextField {
                validator: RegExpValidator {
                    regExp: /[а-яА-ЯІіa-zA-Z]+/
                }
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.lastInputName = text
                    }
                }
            }
            Label {text: "Потужність"}
            TextField {
                validator: DoubleValidator {}
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.power = parseFloat(text)
                    }
                }
            }

            Label {text: "Час роботи"}
            TextField {
                validator: IntValidator {bottom: 0; top: 1000}
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.time_of_work = parseInt(text)
                    }
                }
            }

            Label {text: "Кількість"}
            TextField {
                validator: IntValidator {bottom: 0; top: 1000}
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.quantity = parseInt(text)
                    }
                }
            }

            Label {text: "switch_off_id"}
            TextField {
                validator: IntValidator {bottom: 0; top: 1000}
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.switch_off_id = parseInt(text)
                    }
                }
            }

            Label {text: "switch_on_id"}
            TextField {
                validator: IntValidator {}
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.switch_on_id = parseInt(text)
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
                elecModel.addDevice(lastInputName, power,
                                  time_of_work, quantity,
                                  switch_off_id, switch_on_id)
                break
            case 2:
                shitModel.get(userIndex).name = lastInputName
                shitModel.get(userIndex).power = power
                shitModel.get(userIndex).time_of_work = time_of_work
                shitModel.get(userIndex).quantity = quantity
                shitModel.get(userIndex).switch_off_id = switch_off_id
                shitModel.get(userIndex).switch_on_id = switch_on_id
                break
            case 3:
                evuModel.append({})
                break
            case 4:
//                evuModel.get(userIndex).name = lastInputName
//                shitModel.get(userIndex).power = power
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

    ListModel {
        id: evuModel
    }

}
