import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from script import port
import os

if __name__ == '__main__':

    os.system('python script.py')

    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('view.qml'))
    view.show()

    sys.exit(app.exec_())
