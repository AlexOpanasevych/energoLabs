import sqlite3


class Database:

    def __init__(self, db_path):
        self.db_path = db_path
        self.sqlite_db = sqlite3.connect(self.db_path)
        self.sqlite_db.row_factory = sqlite3.Row
        self.cursor = self.sqlite_db.cursor()

    def user_search(self, actor_name):
        self.cursor.execute('SELECT * FROM electricity_electricaldevices WHERE user.name LIKE \'%{}%\' AND user.lastname LIKE \'%{}%\' ORDER BY user.lastname'.format(actor_name))
        return self.cursor.fetchall()

    def all_users(self):
        self.cursor.execute('SELECT * FROM electricity_electricaldevices')
        return self.cursor.fetchall()


