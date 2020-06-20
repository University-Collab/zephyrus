import pickle
import pymysql as mysql
from controller.data_handler.data_handler import DataHandler


class DBHandler(DataHandler):
    def __init__(self, db, table):
        super().__init__()
        self.db = db
        self.table = table
        self.data = []
        self.db_sessions = []
        self.user = None
        self.password = None
        self.host = None

        self.load_sessions()

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
                cursor.execute("SELECT * FROM %s WHERE id = %s", (self.table, id,))
                self.data = cursor.fetchone()
        finally:
            connection.close()


    def load_sessions(self):
        with open("model/session/connected_dbs", "rb") as sessions:
            self.db_sessions = pickle.load(sessions)
        
        for session in self.db_sessions:
            if session["db"] == self.db:
                self.user = session["user"]
                self.password = session["password"]
                self.host = session["host"]

    def load_data(self):
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
                cursor.execute("SELECT * FROM %s", (self.table,))
                self.data = cursor.fetchall()
            print(self.data)
        finally:
            connection.close()

    def get_all(self):
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
                cursor.execute("SELECT * FROM %s", (self.table,))
                self.data = cursor.fetchall()
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
                cursor.execute("DELETE FROM %s WHERE id = %s", (self.table, id,))
                connection.commit()
        finally:
            connection.close()

    def insert(self, obj):
        pass

    def save(self, data, parent_table=False, sub_table=False):
        pass
