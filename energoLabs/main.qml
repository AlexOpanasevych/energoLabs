import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.0
import QtQuick.Dialogs 1.2
import QtCharts 2.3
import QtWebView 1.1
import Qt.labs.qmlmodels 1.0

Window {
    visible: true
    width: 1280
    height: 720
    title: qsTr("Gzafsgs")

    TabView {
        anchors.fill: parent

        Tab {
            title: "Аналіз метеорологічних даних регіону | Теплотехнічні характеристики будівлі, потреба у тепловій енергії на опалення, ГВП та вентилювання"
            TabView {

                Tab {

                    WebView {
                        anchors.fill: parent
                        url: "http://127.0.0.1:" + 8080
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
                                model: 14;
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
                                    //gmail.func(12)
                                }
                            }
                        }
                    }
                }
                Tab {
                    title: "Звіт 1 new"
                    RowLayout {
                        height: 50
                        Layout.fillWidth: parent.width
                        Button {
                            text: "send"
                            height: 50
                            width : 80
                            //                            onClicked: {
                            //                                gmail.func(12);
                            //                            }
                        }
                        Item {
                            Layout.fillWidth: true
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

                            Component.onCompleted: {
                                var data = dataProvider.thirdGraphData(0, 7)
                                for(let i = 0; i < data.length; i++) {
                                    console.log(data[i].x, data[i].y)
                                    needsGraph.append(new Date(2020, 12, 12 + data[i].x), data[i].y)
//                                    needsGraph.

                                }
                            }
//                            XYPoint {x: 2; y: 10}
//                            XYPoint {x: 4; y: 10}
//                            XYPoint {x: 6; y: 10}
//                            XYPoint {x: 8; y: 10}
//                            XYPoint {x: 10; y: 10}
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
                            Component.onCompleted: {
                                console.log(dg)
                                dg.update_data(genGraph)
                            }
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

                Tab {
                    title: "Звіт 3"
                    RowLayout {
                        height: 50
                        Layout.fillWidth: parent.width
                        Button {
                            text: "send"
                            height: 50
                            width : 80
                            //                            onClicked: {
                            //                                gmail.func(3);
                            //                            }
                        }
                        Item {
                            Layout.fillWidth: true
                        }
                    }
                }


            }


        }
        Tab {
            title: "Визначення ефективності впровадження вітроенергетичної установки для потреб енергозабезпечення об’єкта"
            TabView {
                Tab {
                    id: inputTab
                    property double veuHeight
                    property double veuVelocity
                    property double nextVeuHeight
                    property double veuNextVelocity : veuVelocity * Math.pow((veuHeight / nextVeuHeight), 0.14)
                    title: "Вкладка вводу"
                    Label {text: "Висота башти ВЕУ"}
                    TextField {
                        validator: DoubleValidator {top: 0}
                        onTextChanged: {
                            if(acceptableInput)
                                veuHeight = parseFloat(text)
                        }
                    }
                }

                Tab {
                    ColumnLayout {
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

                        Item {
                            Layout.fillHeight: true
                        }
                    }
                }
                Tab {
                    title: "Завдання 4"
                    TableView {
                        model: TableModel {
                            TableModelColumn {display: "velocity"}
                            TableModelColumn {display: "duration"}
                            TableModelColumn {display: "power"}
                            TableModelColumn {display: "energy"}

                            rows: [
                                {"velocity": 100,
                                    "duration": 2,
                                    "power": 13,
                                    "energy": 2 * 13},
                                {"velocity": 100,
                                    "duration": 2,
                                    "power": 13,
                                    "energy": 2 * 13}

                            ]


                        }
                        TableViewColumn {
                            role: "velocity"
                            title: "Швидкість вітру, м/c"
                            delegate: Text {
                                text: styleData.value  // accessing the property
                            }
                            Component.onCompleted: {
                                console.debug(styleData.value)
                            }
                        }
                        TableViewColumn {
                            role: "duration"
                            title: "Сумарна тривалість, год"
                        }
                        TableViewColumn {
                            role: "power"
                            title: "Потужність ВЕУ, кВт"
                        }
                        TableViewColumn {
                            role: "energy"
                            title: "Енергія вироблена ВЕУ, кВт * год"
                        }

                        //                        itemDelegate: Rectangle {
                        //                            implicitWidth: 100
                        //                            implicitHeight: 50
                        //                            border.width: 1

                        //                            Text {
                        //                                text: display
                        //                                anchors.centerIn: parent
                        //                            }
                        //                        }
                    }

                }
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
                text: inputDialog.lastInputName.toString()
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.lastInputName = text
                    }
                }
            }
            Label {text: "Потужність"}
            TextField {
                validator: DoubleValidator {}
                text: inputDialog.power.toString()
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.power = parseFloat(text)
                    }
                }
            }

            Label {text: "Час роботи"}
            TextField {
                validator: IntValidator {bottom: 0; top: 1000}
                text: inputDialog.time_of_work.toString()
                onTextChanged: {
                    if(acceptableInput) {
                        inputDialog.time_of_work = parseInt(text)
                    }
                }
            }

            Label {text: "Кількість"}
            TextField {
                validator: IntValidator {bottom: 0; top: 1000}
                text: inputDialog.quantity.toString()
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
                elecModel.editDevice(userIndex, lastInputName, power, time_of_work, quantity, switch_off_id, switch_on_id)
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
                elecModel.deleteDevice(userMenu.userIndex)
            }
        }
        MenuItem {
            text: "update info"
            onTriggered: {
                inputDialog.editMode = 2
                //                inputDialog.lastInputName = elecModel.data(userMenu.userIndex, "name")
                //                inputDialog.power = elecModel.data(userMenu.userIndex, "power")
                //                inputDialog.time_of_work = elecModel.data(userMenu.userIndex, "time_of_work")
                //                inputDialog.quantity = elecModel.data(userMenu.userIndex, "quantity")
                inputDialog.open()

            }
        }
    }

    Dialog {

    }

}
