import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from multiprocessing.dummy import Process
import os
from models import *
from data_generator import *
from PyQt5.QtQml import QQmlApplicationEngine

if __name__ == '__main__':

    p = Process(target=os.system, args=('python script.py',))
    p.start()

    dg = data_generator()

    app = QApplication(sys.argv)
#    engine = QQmlApplicationEngine(parent=app)
#    context = engine.rootContext()

    view = QQuickView()
    view.setSource(QUrl('view.qml'))
    ctx = view.rootContext()
    model = ElecModel("lab3.db")
    ctx.setContextProperty('elecModel', model)
    ctx.setContextProperty("dg", dg)
    view.show()
    app.aboutToQuit.connect(lambda: p.join())
    sys.exit(app.exec_())
