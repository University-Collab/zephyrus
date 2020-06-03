import pymysql as mysql
from controller.data_handler import DataHandler


class DBHandler(DataHandler):
    def __init__(self, user, password, db_name, host="localhost", charset="utf8mb4"):
        super().__init__()
        self.user = user
        self.password = password
        self.db = db_name
        self.charset = charset

    def get_one(self, id):
        pass

    def get_all(self):
        pass

    def edit(self, obj):
        pass

    def delete_one(self, id):
        pass

    def insert(self, obj):
        pass

    def save(self, data, parent_table=False, sub_table=False):
        pass
