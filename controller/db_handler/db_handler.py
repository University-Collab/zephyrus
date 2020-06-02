import pymysql as mysql


class DBHandler:
    def __init__(self, user, password, db_name, host="localhost", charset="utf8mb4"):
        super().__init__()
        self.user = user
        self.password = password
        self.db = db_name
        self.charset = charset

    def open_db(self):
        connection = mysql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   db=self.db,
                                   charset=self.charset,
                                   cursorclass=mysql.cursors.DictCursor)

        return connection

    def get_one(self, table_name, search_by, value):
        connection = self.open_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM %s WHERE %s = %s", (
                    table_name,
                    search_by,
                    value,
                ))

                result = cursor.fetchone()

                return result
        finally:
            connection.close()

    def get_all(self, table_name, search_by=None, value=None):
        connection = self.open_db()
        try:
            with connection.cursor() as cursor:
                if search_by is not None:
                    cursor.execute("SELECT * FROM %s WHERE %s = %s", (
                        table_name,
                        search_by,
                        value,
                    ))
                else:
                    cursor.execute("SELECT * FROM %s"),
                    (table_name)

                result = cursor.fetchall()

                return result
        finally:
            connection.close()
