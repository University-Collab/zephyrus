from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy)
from PySide2 import QtGui
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtCore import (QPoint, QModelIndex)


class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.row = 0
        self.column = 0

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

    def delete_row(self):
        self.model().removeRows(self.row, 1, QModelIndex())

    def add_row(self):
        self.model().insertRows(self.row, 1, QModelIndex())