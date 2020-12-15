import QtQuick 2.0
import QtQuick.Controls 1.4
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
            WebEngineView {
                anchors.fill: parent
                url: "http://127.0.0.1:" + 8087
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
