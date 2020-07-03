from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QLineEdit, QComboBox)
from PySide2 import QtGui

class DBManageData(QWidget):
    def __init__(self, referenced_table, parent=None):
        super().__init__(parent)
        self.table = referenced_table

        self.search_layout = QHBoxLayout()

        self.search_text = QLabel()
        self.search_text.setText("Search Table: ")

        self.input_field = QLineEdit()

        self.input_field.setPlaceholderText("Type field value...")
        self.input_field.textChanged.connect(self.search_table)
        self.input_field.returnPressed.connect(self.search_table)

        self.combo_text = QLabel("Search by column: ")
        self.combo_options = QComboBox()
        self.combo_options.insertItem(0, "None chosen")
        self.add_combo_options()
        
        self.search_layout.addWidget(self.search_text)
        self.search_layout.addWidget(self.input_field)
        self.search_layout.addWidget(self.combo_text)
        self.search_layout.addWidget(self.combo_options)

        self.setLayout(self.search_layout)

    def add_combo_options(self):
        list_of_columns = self.table.model().columns
        i = 0
        for column in list_of_columns:
            i += 1
            self.combo_options.insertItem(i, column)

    def search_table(self, line=None):
        if line==None:
            if self.input_field.text() == "":
                return
            input_line = self.input_field.text()
            combo_line = self.combo_options.currentText()
            self.table.model().table_search(input_line, combo_line)
        else:
            combo_line = self.combo_options.currentText()
            self.table.model().table_search(line, combo_line)