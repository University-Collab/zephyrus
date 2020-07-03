from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QDialog, QMessageBox)
from PySide2 import QtGui
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtCore import (QPoint, QModelIndex)

class DBTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.row = 0
        self.column = 0
        self.clicked.connect(self.check_column)

    def check_column(self, index):
        if index.column() == len(self.model().columns) + 1:
            self.delete_row(index.row())

    def add_row(self):
        self.model().insertRows(self.row, 1, QModelIndex())

    def delete_row(self, row=None):
        response = QMessageBox.question(self, "Delete Row?", "Are you sure you want to delete this row?", QMessageBox.Yes | QMessageBox.No)

        if response == QMessageBox.No:
            return
            
        if response == QMessageBox.Yes:
            if row == None:
                self.model().removeRows(self.row, 1, QModelIndex())
            else:
                self.model().removeRows(row, 1, QModelIndex())