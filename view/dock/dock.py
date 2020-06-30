import os, pickle
import pymysql as mysql
from PySide2.QtWidgets import QDockWidget, QFileSystemModel, QTreeView, QLineEdit
from PySide2.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide2.QtCore import QDir
from view.workspace.workspace import Workspace
from view.db_table_dialog.db_table_dialog import DBTableDialog
from view.dock.standard_item import StandardItem


class Dock(QDockWidget):
    def __init__(self, title, central_widget, parent=None):
        super().__init__(title, parent=parent)
        self.central_widget = central_widget

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.tree = QTreeView()

        self.db_tree = QTreeView()
        self.db_model = QStandardItemModel()
        self.db_model.setHorizontalHeaderLabels(["Database"])
        self.db_root = self.db_model.invisibleRootItem()

    def tree_init(self):
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath() + "/model/storage"))

        self.tree.clicked.connect(self.file_clicked)

        self.setWidget(self.tree)

    def init_db_tree(self):
        self.clear_tree()
        self.db_tree.setModel(self.db_model)
        self.setWidget(self.db_tree)
        self.connected_dbs()

    def file_clicked(self, index):
        file_path = self.model.filePath(index)
        workspace = Workspace(file_path, self.central_widget)
        self.central_widget.add_tab(
            workspace,
            QIcon("view/images/dark/baseline_notes_black_48dp.png"),
            file_path.split("storage/")[1],
        )

    def connected_dbs(self):
        if os.path.getsize("model/session/connected_dbs") > 0:
            self.clear_tree()

            with open("model/session/connected_dbs", "rb") as sessions:
                db_sessions = pickle.load(sessions)

            for db in db_sessions:
                connection = mysql.connect(
                    host=db["host"],
                    user=db["user"],
                    password=db["password"],
                    db=db["db"],
                    charset="utf8mb4",
                    cursorclass=mysql.cursors.DictCursor
                )

                temp_db = StandardItem(db["db"], 10, is_bold=True)

                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SHOW TABLES")
                        db_tables = cursor.fetchall()

                    for table in db_tables:
                        for key in table.keys():
                            temp_table = StandardItem(table[key], 9)
                            temp_db.appendRow(temp_table)
                finally:
                    connection.close()

                self.db_root.appendRow(temp_db)
        else:
            no_db = StandardItem("No Connected Databases", 10, is_bold=True)
            self.db_root.appendRow(no_db)

    def table_clicked(self):
        if self.db_tree.currentItem().text() is not None:
            pass

    def clear_tree(self):
        self.db_model.clear()
        self.db_model.setHorizontalHeaderLabels(["Database"])
        self.db_root = self.db_model.invisibleRootItem()
