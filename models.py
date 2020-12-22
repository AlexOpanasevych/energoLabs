import database
from PyQt5.QtCore import QAbstractListModel, Qt, pyqtSlot, QModelIndex


class ElecModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    PowerRole = Qt.UserRole + 2
    TimeOfWorkRole = Qt.UserRole + 3
    QuantityRole = Qt.UserRole + 4
    SwitchOffIdRole = Qt.UserRole + 5
    SwitchOnIdRole = Qt.UserRole + 6
    _roles = {NameRole: b"name", PowerRole: b"power", TimeOfWorkRole: b"time_of_work", \
    QuantityRole: b"quantity", SwitchOffIdRole: b"swith_off_id", SwitchOnIdRole: b"swith_on_id"}

    def __init__(self, db_path):
        super(ElecModel, self).__init__()
        self._actors = []
        self._db = database.Database(db_path)
        self.update("")

    def update(self, search_term : str):
        self.beginResetModel()
        if search_term:
            self._actors = self._db.user_search(search_term)
        else:
            self._actors = self._db.all_users()
        self.endResetModel()

    @pyqtSlot(str, float, int, int, int, int)
    def addDevice(self, name, power, time_of_work, quantity, switch_off_id, switch_on_id):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._actors.append({"name" : name, "power" : power, "time_of_work": time_of_work, "quantity" : quantity, "switch_off_id": switch_off_id, "switch_on_id": switch_on_id})
        self.endInsertRows()

    @pyqtSlot(int, str, float, int, int, int, int)
    def editDevice(self, row, name, power, time_of_work, quantity, switch_off_id, switch_on_id):
        ix = self.index(row, 0)
        self.persons[row] = {"name" : name, "power" : power, "time_of_work": time_of_work, "quantity" : quantity, "switch_off_id": switch_off_id, "switch_on_id": switch_on_id}
        self.dataChanged.emit(ix, ix, self.roleNames())

    @pyqtSlot(int)
    def deleteDevice(self, row):
        self.beginRemoveColumns(QModelIndex(), row, row)
        del self._actors[row]
        self.endRemoveRows()

    # Reacts to onTextChanged event of searchBar (in QML code)
    @pyqtSlot(str)
    def search_input(self, search_input):
        if len(search_input) > 3:
            print(search_input)
        self.update(search_input)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._actors)

    def data(self, QModelIndex, role=None):
        row = QModelIndex.row()
        if role == self.NameRole:
            return self._actors[row]["name"]

        if role == self.PowerRole:
            return self._actors[row]["power"]
        if role == self.TimeOfWorkRole:
            return self._actors[row]["time_of_work"]
        if role == self.QuantityRole:
            return self._actors[row]["quantity"]
        if role == self.SwitchOnIdRole:
            return self._actors[row]["swith_on_id"]

        if role == self.SwitchOffIdRole:
            return self._actors[row]["swith_off_id"]

    @pyqtSlot(int, str)
    def getData(self, row, role):
        return self._actors[row][role]


    def roleNames(self):
        return self._roles

#class EvuModel(QAbstractListModel):
#    NameRole = Qt.UserRole + 1
#    PowerRole = Qt.UserRole + 2
#    TimeOfWorkRole = Qt.UserRole + 3
#    QuantityRole = Qt.UserRole + 4
#    SwitchOffIdRole = Qt.UserRole + 5
#    SwitchOnIdRole = Qt.UserRole + 6
#    _roles = {NameRole: b"name", PowerRole: b"power", TimeOfWorkRole: b"time_of_work", \
#    QuantityRole: b"quantity", SwitchOffIdRole: b"swith_off_id", SwitchOnIdRole: b"swith_on_id"}

#    def __init__(self, db_path):
#        super(EvuModel, self).__init__()
#        self._actors = []
#        self._db = database.Database(db_path)
#        self.update("")

#    def update(self, search_term : str):
#        self.beginResetModel()
#        if search_term:
#            self._actors = self._db.user_search(search_term)
#        else:
#            self._actors = self._db.all_users()
#        self.endResetModel()

#    @pyqtSlot(str, float, int, int, int, int)
#    def addDevice(self, name, power, time_of_work, quantity, switch_off_id, switch_on_id):
#        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
#        self._actors.append({"name" : name, "power" : power, "time_of_work": time_of_work, "quantity" : quantity, "switch_off_id": switch_off_id, "switch_on_id": switch_on_id})
#        self.endInsertRows()

#    @pyqtSlot(int, str, float, int, int, int, int)
#    def editDevice(self, row, name, power, time_of_work, quantity, switch_off_id, switch_on_id):
#        ix = self.index(row, 0)
#        self.persons[row] = {"name" : name, "power" : power, "time_of_work": time_of_work, "quantity" : quantity, "switch_off_id": switch_off_id, "switch_on_id": switch_on_id}
#        self.dataChanged.emit(ix, ix, self.roleNames())

#    @pyqtSlot(int)
#    def deleteDevice(self, row):
#        self.beginRemoveColumns(QModelIndex(), row, row)
#        del self._actors[row]
#        self.endRemoveRows()

#    # Reacts to onTextChanged event of searchBar (in QML code)
#    @pyqtSlot(str)
#    def search_input(self, search_input):
#        if len(search_input) > 3:
#            print(search_input)
#        self.update(search_input)

#    def rowCount(self, parent=None, *args, **kwargs):
#        return len(self._actors)

#    def data(self, QModelIndex, role=None):
#        row = QModelIndex.row()
#        if role == self.NameRole:
#            return self._actors[row]["name"]

#        if role == self.PowerRole:
#            return self._actors[row]["power"]
#        if role == self.TimeOfWorkRole:
#            return self._actors[row]["time_of_work"]
#        if role == self.QuantityRole:
#            return self._actors[row]["quantity"]
#        if role == self.SwitchOnIdRole:
#            return self._actors[row]["swith_on_id"]

#        if role == self.SwitchOffIdRole:
#            return self._actors[row]["swith_off_id"]

#    @pyqtSlot(int, str)
#    def getData(self, row, role):
#        return self._actors[row][role]


#    def roleNames(self):
#        return self._roles
