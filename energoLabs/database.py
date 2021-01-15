import sqlite3
from PyQt5.QtWidgets import QMessageBox

class Database:

    def __init__(self, db_path):
        self.db_path = db_path
        self.sqlite_db = sqlite3.connect(self.db_path)
        self.sqlite_db.row_factory = sqlite3.Row
        self.cursor = self.sqlite_db.cursor()

    def user_search(self, actor_name):
        self.cursor.execute('''SELECT * FROM electricity_electricaldevices
                            WHERE name LIKE \'%{}%\'
                            ORDER BY user.name'''.format(actor_name))
        return self.cursor.fetchall()

    def all_users(self):
        self.cursor.execute('SELECT * FROM electricity_electricaldevices')
        return self.cursor.fetchall()

    def getCountElectricalDevices(self):
        self.cursor.execute('SELECT name, count FROM electricity_electricaldevices')
        return self.cursor.fetchall()

    def getPowerElectricalDevices(self):
        self.cursor.execute('SELECT power FROM electricity_electricaldevices')
        return self.cursor.fetchall()

    def addDevice(self, name, power, time_of_work,
                  switch_off_id, switch_on_id):
#        info = [name, power, time_of_work, switch_off_id, switch_on_id]
        query = '''INSERT INTO electricity_electricaldevices (name, power, time_of_work, switch_off_id, switch_on_id) VALUES ('{}', {}, {}, {}, {})'''.format(name, power, time_of_work, switch_off_id, switch_on_id)
        self.cursor.execute(query)

    def removeDevice(self, id):
        dialog = QMessageBox()
        dialog.setText(str(id))
        dialog.exec_()
        self.cursor.execute('DELETE FROM electricity_electricaldevices WHERE id = {}'.format(id))

    def updateDevice(self, id, name, power, switch_off_id, switch_on_id):
        info = [name, power, switch_off_id, switch_on_id, id]
        self.cursor.execute('''UPDATE electricity_electricaldevices
        SET name = ?, power = ?, switch_off_id = ?, switch_on_id = ?
        WHERE id = ?''', info)
