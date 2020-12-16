import database
from PyQt5.QtCore import QAbstractListModel, Qt, pyqtSlot


class UserModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    LastnameRole = Qt.UserRole + 2

    _roles = {NameRole: b"name", LastnameRole: b"thumb"}

    def __init__(self, db_path):
        super(UserModel, self).__init__()
        self._actors = []
        self._db = database.Database(db_path)

    def update(self, search_term : str):
        self.beginResetModel()
        if search_term:
            self._actors = self._db.user_search(search_term)
        else:
            self._actors = self._db.all_users()
        self.endResetModel()

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

        if role == self.ThumbRole:
            return self._actors[row]["thumbnail"]

    def roleNames(self):
        return self._roles
