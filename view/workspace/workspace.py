import json, pickle
from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QLineEdit, QComboBox, QListWidget, QToolBar)
                               
from PySide2 import QtGui
from PySide2.QtGui import QIcon

from controller.serial_data_handler.serial_data_handler import SerialDataHandler
from controller.sequential_data_handler.sequential_data_handler import (
    SequentialDataHandler, )
from model.table_model.table_model import TableModel
from view.table_view.table_view import TableView
from view.section_manage_data.manage_data import ManageData
from view.section_add_data.add_data import AddData


class Workspace(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout()
        self.tab_widget = None
        self.file_path = file_path
        self.meta_path = None
        self.subtable_meta_path = None
        self.subtable_path = None
        self.handler_type = None
        self.handler = None
        self.table_model = None
        self.meta_data = None
        self.create_tab_widget()

        # for table
        self.main_table = TableView(self.tab_widget)
        self.main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.create_model()
        self.main_table.clicked.connect(self.row_selected)

        # package
        self.package = QVBoxLayout()
        
        self.comboWidget = QComboBox()
        
        self.comboWidget.insertItem(0, "None chosen")
        self.comboWidget.insertItem(1, "Manage Data")
        self.comboWidget.insertItem(2, "Add Data")
        # manage data
        self.manageData = ManageData(self.main_table)
        # add data
        self.addData = AddData(self.main_table)
        # stacked layer
        self.stackedLayout = QStackedLayout()
        self.label = QLabel()
        self.label.setText("Work with data, choose state.")
        self.stackedLayout.addWidget(self.label)
        self.stackedLayout.addWidget(self.manageData)
        self.stackedLayout.addWidget(self.addData)
        self.stackedLayout.setCurrentIndex(0)

        self.comboWidget.activated.connect(self.stackedLayout.setCurrentIndex)

        self.package.addWidget(self.comboWidget)
        self.package.addLayout(self.stackedLayout)
        self.package.addWidget(self.main_table)
        

        self.main_layout.addLayout(self.package)
     
        self.setLayout(self.main_layout)



    def handler_type_check(self):
        self.subtable_path = self.file_path.split("storage/")[0] + "storage/" + self.meta_data["linked file"]
        self.subtable_meta_path = self.file_path.split("storage/")[0] + "meta/" + self.meta_data["linked file"] + "_metadata.json"
        with open(self.subtable_meta_path, "r") as meta_data:
            data = json.load(meta_data)
            if data["handler type"] == "serial":
                return "serial"
            else:
                return "sequential"

    def create_model(self):
        temp = self.file_path.split("storage/")
        self.meta_path = temp[0] + "meta/" + temp[1].split(
            ".")[0] + "_metadata.json"
        with open(self.meta_path) as metadata:
            data = json.load(metadata)
            self.meta_data = data
            self.handler_type = data["handler type"]

        if self.handler_type == "serial":
            self.handler = SerialDataHandler(self.file_path, self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

        if self.handler_type == "sequential":
            self.handler = SequentialDataHandler(self.file_path,
                                                 self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

    def row_selected(self, index):

        
        if index.column() == len(self.main_table.model().metadata["columns"]):
            return 

        model = self.main_table.model()
        selected_data = model.get_element(index)

        type = self.handler_type_check()
        unique_data = selected_data[self.meta_data["search key"]]

        if type == "serial":
            subtable_model = TableModel(
                SerialDataHandler(self.subtable_path, self.subtable_meta_path,
                                  unique_data))
        else:
            subtable_model = TableModel(
                SequentialDataHandler(self.file_path, self.meta_path,
                                      unique_data))

        subtable = TableView(self.tab_widget)
        subtable.setModel(subtable_model)

        # package
        package = QVBoxLayout()
        
        comboWidget = QComboBox()
        comboWidget.insertItem(0, "None choosen.")
        comboWidget.insertItem(1, "Manage Data")
        comboWidget.insertItem(2, "Add Data")
        # manage data
        manageData = ManageData(subtable)
        # add data
        addData = AddData(subtable)
        # stacked layer
        stackedLayout = QStackedLayout()
        stackedLayout.addWidget(self.label)
        stackedLayout.addWidget(manageData)
        stackedLayout.addWidget(addData)
        stackedLayout.setCurrentIndex(0)

        comboWidget.activated.connect(stackedLayout.setCurrentIndex)

        package.addWidget(comboWidget)
        package.addLayout(stackedLayout)
        package.addWidget(subtable)

        widg_ = QWidget()
        widg_.setLayout(package)

        self.tab_widget.addTab(widg_, self.meta_data["additional tab name"])
        self.main_layout.addWidget(self.tab_widget)

    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

