import os, pickle
import pymysql as mysql
from PySide2.QtWidgets import QDockWidget, QFileSystemModel, QTreeView, QLineEdit, QMenu, QAction, QMessageBox, QPushButton
from PySide2.QtGui import QIcon, QStandardItemModel, QStandardItem
from PySide2.QtCore import QDir, Qt
from view.workspace.workspace import Workspace
from view.workspace.db_workspace import DBWorkspace
from view.dock.standard_item import StandardItem


class Dock(QDockWidget):
    def __init__(self, title, central_widget, parent=None):
        super().__init__(title, parent=parent)
        self.central_widget = central_widget

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.tree = QTreeView()
        self.tree.pressed.connect(self.setIndex)
        self.index_ = None

        self.db_tree = QTreeView()
        self.db_tree.setAnimated(True)
        self.db_model = QStandardItemModel()
        self.db_model.setHorizontalHeaderLabels(["Database"])
        self.db_root = self.db_model.invisibleRootItem()

        self.dbs = []

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        deleteFile = contextMenu.addAction("Delete File")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == deleteFile:
            alert = QMessageBox()
            alert.setWindowTitle("Action Dialog")
            alert.setText("Are you sure you want to delete this file?")
            alert.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            alert.setDefaultButton(QMessageBox.No)
            response = alert.exec_()
            if response == QMessageBox.No:
                contextMenu.close()
            else:
                file_name = self.model.filePath(self.index_).split("storage/")[1]
                os.remove(self.model.filePath(self.index_))
                os.remove(self.model.filePath(self.index_).split("/storage")[0] + "/meta/" + file_name + "_metadata.json")
                contextMenu.close()


    def setIndex(self, index):
        self.index_ = index

    def tree_init(self):
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath() + "/model/storage"))

        self.tree.clicked.connect(self.file_clicked)

        self.setWidget(self.tree)

    def init_db_tree(self):
        self.clear_tree()
        self.db_tree.setModel(self.db_model)
        self.db_tree.clicked.connect(self.table_clicked)
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
        if os.path.exists("model/session/connected_dbs") and os.path.getsize("model/session/connected_dbs") > 0:
            self.clear_tree()

            self.dbs = []

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

                self.dbs.append(db["db"])

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
            self.clear_tree()
            self.dbs = []
            no_db = StandardItem("No Connected Databases", 10, is_bold=True)
            self.db_root.appendRow(no_db)

    def table_clicked(self, val):
        self.is_db = False
        if os.path.exists("model/session/connected_dbs") and len(self.dbs) != 0:
            for db in self.dbs:
                if db == val.data():
                    self.is_db = True

                    remove_choice = QMessageBox.question(self.db_tree, "Disconnect Database", f'Do you want to remove "{val.data()}" from connected databases?', QMessageBox.Yes | QMessageBox.No)

                    if remove_choice == QMessageBox.Yes:
                        with open("model/session/connected_dbs", "rb") as sessions:
                            db_sessions = pickle.load(sessions)
                
                        db_sessions[:] = [db for db in db_sessions if db.get('db') != val.data()]

                        for db in db_sessions:
                            if db["index"] != 1:
                                db["index"] -= 1

                        self.dbs[:] = [db for db in self.dbs if db != val.data()]

                        if len(db_sessions) == 0:
                            os.remove("model/session/connected_dbs")
                        else:
                            with open("model/session/connected_dbs", "wb") as sessions:
                                pickle.dump(db_sessions, sessions)

                        QMessageBox.information(self.db_tree, "(㇏(•̀ᵥᵥ•́)ノ)", f'Database "{val.data()}" successfully disconnected.', QMessageBox.Ok)
                        self.connected_dbs()
                        break

                    if remove_choice == QMessageBox.No:
                        break
            
            if not self.is_db:
                user_reply = QMessageBox.question(self.db_tree, "Answer. Thanks.", f'Do you want to open the "{val.data()}" table?', QMessageBox.Open | QMessageBox.Cancel)

                if user_reply == QMessageBox.Cancel:
                    pass
                
                if user_reply == QMessageBox.Open:
                    workspace = DBWorkspace(val.parent().data() ,val.data(), self.central_widget)
                    self.central_widget.add_tab(
                        workspace,
                        QIcon("view/images/menubar/database-connect.png"),
                        val.data(),
                    )

    def clear_tree(self):
        self.db_model.clear()
        self.db_model.setHorizontalHeaderLabels(["Database"])
        self.db_root = self.db_model.invisibleRootItem()
