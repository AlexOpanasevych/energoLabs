# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from models import *
from PyQt5.QtChart import *
import random

class data_generator(QtCore.QObject):
    def __init__(self, parent = None):
        super(data_generator, self).__init__(parent)
        self.data = []
        self.index = -1

    @pyqtSlot(QAbstractSeries)
    def update_data(self, series):
        print("Here we go")
        for i in range(7):
            series.append(i, random.randint(200, 1000))
