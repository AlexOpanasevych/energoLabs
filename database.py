import sqlite3


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
                  count, switch_off_id, switch_on_id):
        info = [name, power, count, switch_off_id, switch_on_id]
        query = 'INSERT INTO electricity_electricaldevices (name, power, count, switch_off_id, switch_on_id) VALUES ({})'.format(", ".join(str(item) for item in info))
        print(query)
        self.cursor.execute(query)

    def removeDevice(self, id, count):
        current_count = self.cursor.execute('SELECT count FROM \
                            electricity_electricaldevices WHERE id=?', id)
        info = [current_count - count, id]
        if current_count == count:
            self.cursor.execute('DELETE FROM electricity_electricaldevices \
            WHERE id=?', id)
        else:
            self.cursor.execute('''UPDATE electricity_electricaldevices
            SET count = ?
            WHERE id = ?''', info)

    def updateDevice(self, id, name, power,
                     count, switch_off_id, switch_on_id):
        info = [name, power, count, switch_off_id, switch_on_id, id]
        self.cursor.execute('''UPDATE electricity_electricaldevices
        SET name = ?, power = ?, count = ?, switch_off_id = ?, switch_on_id = ?
        WHERE id = ?''', info)
