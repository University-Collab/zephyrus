from PySide2.QtWidgets import QDockWidget, QFileSystemModel, QTreeView, QLineEdit
from PySide2.QtGui import QIcon
from PySide2.QtCore import QDir
from workspace.workspace import Workspace


class Dock(QDockWidget):
    def __init__(self, title, central_widget, parent=None):
        super().__init__(title, parent=parent)

        self.central_widget = central_widget
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        # treba nam metoda koja ce vracati apsolutnu putanju za dati direktorijum kako bi bilo kompatibilno i za Linuks
        self.tree.setRootIndex(self.model.index(QDir.currentPath() + "\storage")) 

        self.tree.clicked.connect(self.file_clicked)

        self.setWidget(self.tree)

    def file_clicked(self, index):
        # kreira se workspace i dodaje central widgetu
        file_path = self.model.filePath(index)
        workspace = Workspace(file_path, self.central_widget)
        self.central_widget.add_tab(workspace, QIcon("../images/logo/zephyrus_icon.png"), "Statistic data")
