import pickle
import pymysql as mysql
from controller.data_handler.data_handler import DataHandler


class DBHandler(DataHandler):
    def __init__(self, db, table):
        super().__init__()
        self.db = db
        self.table = table
        self.data = []
        self.columns = []
        self.db_sessions = []
        self.user = None
        self.password = None
        self.host = None

        self.load_sessions()
        self.load_data()

    def load_sessions(self):
        with open("model/session/connected_dbs", "rb") as sessions:
            self.db_sessions = pickle.load(sessions)
        
        for session in self.db_sessions:
            if session["db"] == self.db:
                self.user = session["user"]
                self.password = session["password"]
                self.host = session["host"]

    def load_data(self):
        self.get_all()

    def get_one(self, id):
        connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4",
            cursorclass=mysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM " + self.table + " WHERE id = " + id)
                self.data = cursor.fetchone()

                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='" + self.db + "'" + " AND " + "table_name='" + self.table + "' WHERE id=" + id)
                temp = cursor.fetchall()
                
                for column in temp:
                    self.columns.append(column["COLUMN_NAME"])
            if len(self.data) == 0:
                return None
            else:
                return self.data
        finally:
            connection.close()

    def get_all(self):
        self.columns = []
        connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4",
            cursorclass=mysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM " + self.table)
                self.data = cursor.fetchall()

                cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='" + self.db + "'" + " AND " + "table_name='" + self.table + "'")
                temp = cursor.fetchall()
                
                for column in temp:
                    self.columns.append(column["COLUMN_NAME"])
        finally:
            connection.close()

    def edit(self, obj):
        connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4",
            cursorclass=mysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # TODO: cursor.execute("UPDATE %s SET %s = %s WHERE id = %s", (self.table, , obj))
                connection.commit()
        finally:
            connection.close()

    def delete_one(self, id):
        connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4",
            cursorclass=mysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM " + self.table + " WHERE id = " + id)
                connection.commit()
        finally:
            connection.close()

    def insert(self, obj):
        connection = mysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            charset="utf8mb4",
            cursorclass=mysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO " + self.table + " VALUES " + "(" + obj + ")")
                connection.commit()
        finally:
            connection.close()

    def save(self, data, parent_table=False, sub_table=False):
        pass
