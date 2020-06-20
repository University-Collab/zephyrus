import pickle
import pymysql as mysql
from PySide2.QtWidgets import QDialog, QListWidget, QVBoxLayout, QLabel
from controller.db_handler.db_handler import DBHandler

class DBTableDialog(QDialog):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.tables = QListWidget()

    def display_tables(self):
        with open("model/session/connected_dbs", "rb") as sessions:
            db_sessions = pickle.load(sessions)

        for db in db_sessions:
            if db["db"] == self.db:
                connection = mysql.connect(
                    host=db["host"],
                    user=db["user"],
                    password=db["password"],
                    db=db["db"],
                    charset="utf8mb4",
                    cursorclass=mysql.cursors.DictCursor
                )
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SHOW TABLES")
                        db_tables = cursor.fetchall()

                    for table in range(len(db_tables)):
                        self.tables.insertItem(table, db_tables[table]["Tables_in_higher-education-institution"])

                    self.tables.itemClicked.connect(self.table_selected)
                finally:
                    connection.close()

        layout = QVBoxLayout()

        info_label = QLabel("Select a table you want to display")

        layout.addWidget(info_label)
        layout.addWidget(self.tables)

        self.setLayout(layout)

        self.setWindowTitle("Select Table")
        self.setModal(True)
        self.show()

    def table_selected(self):
        if self.tables.currentItem().text() is not None:
            db_handler = DBHandler(self.db, self.tables.currentItem().text())
            db_handler.load_data() # test
