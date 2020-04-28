from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTabWidget,
    QTableView,
    QAbstractItemView,
    QLineEdit,
    QMenu,
    QAction,
    QSizePolicy
)
from PySide2 import QtGui
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtCore import (
    QPoint,
    QModelIndex
)

class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.row = 0
        self.column = 0
        # self.model = self.model()

    def contextMenuEvent(self, event):
        self.row = self.rowAt(event.y())
        self.column = self.columnAt(event.x())
       
        # indeks = model.index(row, column)
        # selected_data = model.get_element(indeks)
        # print(selected_data)

        if self.row == -1 or self.column == -1:
            return 
        else :
            self.menu = QMenu(self)
            addRow = QAction('Add new row', self)
            deleteRow = QAction('Remove row', self)

            addRow.triggered.connect(self.add_row)
            # deleteRow.triggered.connect(lambda: self.remove_row(selected_data))
            deleteRow.triggered.connect(self.delete_row) 


            self.menu.addAction(addRow)
            self.menu.addAction(deleteRow)

            self.menu.popup(QtGui.QCursor.pos())
        
    def delete_row(self):
        self.model().removeRows(self.row, 1, QModelIndex())

    def add_row(self):
        self.model().insertRows(self.row, 1, QModelIndex())