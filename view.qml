import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import QtWebEngine 1.10

Item {
    id: root
    width: 1280
    height: 700
    //visibility: "Maximized"
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
                        contentWidth: column.width    // The important part
                        contentHeight: column.height  // Same
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
                                        source: "images/first_lab/" + (index+1) + ".png"
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
        }

        Tab {
            title: "Визначення ефективності впровадження вітроенергетичної установки для потреб енергозабезпечення об’єкта"
        }
        Tab {
            title: "Визначення ефективності впровадження повітряного теплового насосу для потреб систем опалення та кондиціонування об’єкта"
        }
    }
}
