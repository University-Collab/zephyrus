import json
from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTabWidget,
    QTableView,
    QAbstractItemView,
    QLineEdit,
)

from controller.serial_data_handler.serial_data_handler import SerialDataHandler
from controller.sequential_data_handler.sequential_data_handler import (
    SequentialDataHandler, )
from model.table_model.table_model import TableModel


class Workspace(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout()
        self.tab_widget = None
        self.file_path = file_path
        self.meta_path = None
        self.handler_type = None
        self.handler = None
        self.table_model = None
        self.meta_data = None
        self.create_tab_widget()

        self.main_table = QTableView(self.tab_widget)
        self.main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.create_model()

        self.main_table.clicked.connect(self.row_selected)

        self.main_layout.addWidget(self.main_table)
        self.main_layout.addWidget(self.tab_widget)
        self.setLayout(self.main_layout)

    def handler_type_check(self):
        with open(self.meta_path) as metadata:
            data = json.load(metadata)
            self.meta_data = data
            if data["handler type"] == "serial":
                return "serial"
            elif data["handler type"] == "sequential":
                return "sequential"

    def create_model(self):
        temp = self.file_path.split("storage/")
        self.meta_path = temp[0] + "meta/" + temp[1].split(".")[0] + "_metadata.json"
        with open(self.meta_path) as metadata:
            data = json.load(metadata)
            self.meta_data = data
            self.handler_type = self.handler_type_check()

        if self.handler_type == "serial":
            self.handler = SerialDataHandler(self.file_path, self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

        if self.handler_type == "sequential":
            self.handler = SequentialDataHandler(self.file_path, self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

    def row_selected(self, index):
        model = self.main_table.model()
        selected_data = model.get_element(index)

        type = self.handler_type_check()
        unique_data = selected_data[self.meta_data["search key"]]

        if type == "serial":
            subtable_model = TableModel(SerialDataHandler(self.file_path, self.meta_path, False, unique_data))
        else:
            subtable_model = TableModel(SequentialDataHandler(self.file_path, self.meta_path, False, unique_data))

        subtable = QTableView(self.tab_widget)
        subtable.setModel(subtable_model)
        self.tab_widget.addTab(subtable, self.meta_data["additional tab name"])

    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)
