from PySide2.QtWidgets import QDockWidget, QFileSystemModel, QTreeView
from PySide2.QtCore import QDir


class Dock(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent=parent)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))

        self.setWidget(self.tree)
