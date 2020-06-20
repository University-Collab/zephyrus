import os, pickle
from PySide2.QtWidgets import QDockWidget, QFileSystemModel, QTreeView, QLineEdit, QListWidget
from PySide2.QtGui import QIcon
from PySide2.QtCore import QDir
from view.workspace.workspace import Workspace
from view.db_table_dialog.db_table_dialog import DBTableDialog


class Dock(QDockWidget):
    def __init__(self, title, central_widget, parent=None):
        super().__init__(title, parent=parent)
        self.central_widget = central_widget
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.tree = QTreeView()
        self.list = QListWidget()

    def tree_init(self):
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath() + "/model/storage"))

        self.tree.clicked.connect(self.file_clicked)

        self.setWidget(self.tree)

    def list_init(self):
        self.setWidget(self.list)
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
            self.list.clear()
            with open("model/session/connected_dbs", "rb") as sessions:
                db_sessions = pickle.load(sessions)

            for db in db_sessions:
                self.list.insertItem(db["index"], db["db"])

            self.list.itemClicked.connect(self.db_clicked)
        else:
            self.list.clear()
            self.list.insertItem(0,"No Databases Connected")

    def db_clicked(self):
        if self.list.currentItem().text() is not None:
            table_dialog = DBTableDialog(self, self.list.currentItem().text())
            table_dialog.display_tables()
        
