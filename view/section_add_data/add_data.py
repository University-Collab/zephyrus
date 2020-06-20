from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QLineEdit, QComboBox)
from PySide2 import QtGui

class AddData(QWidget):
    def __init__(self, referenced_table, parent=None):
        super().__init__(parent)
        self.table = referenced_table
        self.layout = QVBoxLayout()

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

        self.form = QFormLayout()
        for column in self.table.model().metadata['columns']:
            self.form.addRow(column, QLineEdit())
        self.button = QPushButton("add")
        self.button.clicked.connect(self.add_row)
        self.fresh_button = QPushButton("start fresh")
        self.fresh_button.clicked.connect(self.clean)
        self.form.addWidget(self.button)
        self.form.addWidget(self.fresh_button)
        self.fresh_button.setVisible(False)

        self.layout.addLayout(self.search_layout)
        self.layout.addLayout(self.form)
        self.setLayout(self.layout)

    def add_row(self):
        obj = {}
        i = 0
        j = 0
        while i < 2*len(self.table.model().metadata["columns"]):
            obj[self.table.model().metadata["columns"][j]] = self.form.itemAt(i+1).widget().text()
            j +=1
            i +=2
        print(obj)
        self.table.model().insert_row(obj)
        self.fresh_button.setVisible(True)

    def clean(self):
        i = 0
        while i < 2*len(self.table.model().metadata["columns"]):
            self.form.itemAt(i+1).widget().setText("")
            i+=2

    def add_combo_options(self):
        list_of_columns = self.table.model().metadata["columns"]
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