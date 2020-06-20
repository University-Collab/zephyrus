from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QDialog, QMessageBox)
from PySide2 import QtGui
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtCore import (QPoint, QModelIndex)


class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.row = 0
        self.column = 0
        self.clicked.connect(self.check_column)
    

    def check_column(self, index):
        if index.column() == len(self.model().metadata["columns"])+1:
            self.delete_row(index.row())

    def contextMenuEvent(self, event):
        self.row = self.rowAt(event.y())
        self.column = self.columnAt(event.x())

        if self.row == -1 or self.column == -1:
            return
        else:
            self.menu = QMenu(self)
            addRow = QAction('Add new row', self)
            deleteRow = QAction('Remove row', self)

            addRow.triggered.connect(self.add_row)
            deleteRow.triggered.connect(self.delete_row)

            self.menu.addAction(addRow)
            self.menu.addAction(deleteRow)
            self.menu.popup(QtGui.QCursor.pos())

    def delete_row(self, row=None):
        alert = QMessageBox()
        alert.setWindowTitle("Action Dialog")
        alert.setText("Are you sure you want to delete this row?")
        alert.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        alert.setDefaultButton(QMessageBox.No)
        response = alert.exec_()
        if response == QMessageBox.No:
            return
        else: 
            if row == None:
                self.model().removeRows(self.row, 1, QModelIndex())
            else:
                self.model().removeRows(row, 1, QModelIndex())

    def add_row(self):
        self.model().insertRows(self.row, 1, QModelIndex())