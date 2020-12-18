import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from multiprocessing.dummy import Process
import os

if __name__ == '__main__':

    p = Process(target=os.system, args=('python script.py',))
    p.start()

    app = QApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('view.qml'))
    view.show()
    app.aboutToQuit.connect(lambda: p.join())
    sys.exit(app.exec_())
