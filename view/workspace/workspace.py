import json, pickle
from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QLineEdit, QComboBox, QListWidget, QToolBar, QMessageBox)
                               
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

        self.main_table = TableView(self.tab_widget)
        self.main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.create_model()
        self.main_table.clicked.connect(self.row_selected)

        self.package = QVBoxLayout()
        
        self.toolBar = QToolBar()
        self.toolBar.setMovable(True)
        
        self.toolBar.addAction(QIcon("view/images/toolbar/list_48px.png"), "Manage Data")
        self.toolBar.addAction(QIcon("view/images/toolbar/add_new_40px.png"), "Add Data")
        self.toolBar.addAction(QIcon("view/images/toolbar/close_window_26px.png"), "Close")

        self.manageData = ManageData(self.main_table)

        self.addData = AddData(self.main_table)

        self.stackedLayout = QStackedLayout()
        self.label = QLabel()
        self.label.setText("Work with data, choose state.")
        self.stackedLayout.addWidget(self.label)
        self.stackedLayout.addWidget(self.manageData)
        self.stackedLayout.addWidget(self.addData)
        self.stackedLayout.setCurrentIndex(0)

        self.toolBar.actionTriggered.connect(self.setStackedLayout)

        self.package.addWidget(self.toolBar)
        self.package.addLayout(self.stackedLayout)
        self.package.addWidget(self.main_table)
        
        self.main_layout.addLayout(self.package)
     
        self.setLayout(self.main_layout)

    def setStackedLayout(self, action):
        if action.iconText() == "Manage Data":
            self.stackedLayout.setCurrentIndex(1)
        
        elif action.iconText() == "Add Data":
            self.stackedLayout.setCurrentIndex(2)

        elif action.iconText() == "Close":
            self.stackedLayout.setCurrentIndex(0)

    def set_paths(self):
        self.subtable_path = self.file_path.split("storage/")[0] + "storage/" + self.meta_data["linked file"]
        self.subtable_meta_path = self.file_path.split("storage/")[0] + "meta/" + self.meta_data["linked file"] + "_metadata.json"

    def create_model(self): 
        temp = self.file_path.split("storage/")
        self.meta_path = temp[0] + "meta/" + temp[1].split(
            ".")[0] + "_metadata.json"
        with open(self.meta_path) as metadata:
            data = json.load(metadata)
            self.meta_data = data

        handler = QMessageBox()
        handler.setWindowTitle("Need for speed?")
        handler.setText("Is there a need for fast sequential file handling?")
        handler.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        handler.setDefaultButton(QMessageBox.No)
        user_reply = handler.exec_()

        if user_reply == QMessageBox.No:
            self.handler = SerialDataHandler(self.file_path, self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

        if user_reply == QMessageBox.Yes:
            self.handler = SequentialDataHandler(self.file_path,
                                                self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

    def row_selected(self, index):
        if index.column() == len(self.main_table.model().metadata["columns"]):

            model = self.main_table.model()
            selected_data = model.get_element(index)

            self.set_paths()
            unique_data = selected_data[self.meta_data["search key"]]            

            handler = QMessageBox()
            handler.setWindowTitle("Need for speed?")
            handler.setText("Is there a need for fast sequential file handling?")
            handler.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            handler.setDefaultButton(QMessageBox.No)
            user_reply = handler.exec_()

            if user_reply == QMessageBox.No:
                subtable_model = TableModel(
                    SerialDataHandler(self.subtable_path, self.subtable_meta_path,
                                    unique_data))

            if user_reply == QMessageBox.Yes:
                subtable_model = TableModel(
                    SequentialDataHandler(self.subtable_path, self.subtable_meta_path,
                                        unique_data))

            subtable = TableView(self.tab_widget)
            subtable.setModel(subtable_model)

            package = QVBoxLayout()

            toolBar = QToolBar()
            toolBar.setMovable(True)
            
            toolBar.addAction(QIcon("view/images/list_48px.png"), "Manage Data")
            toolBar.addAction(QIcon("view/images/add_new_40px.png"), "Add Data")
            toolBar.addAction(QIcon("view/images/close_window_26px.png"), "Close")

            manageData = ManageData(subtable)

            addData = AddData(subtable)

            self.stackedLayout2 = QStackedLayout()
            self.stackedLayout2.addWidget(self.label)
            self.stackedLayout2.addWidget(manageData)
            self.stackedLayout2.addWidget(addData)
            self.stackedLayout2.setCurrentIndex(0)

            toolBar.actionTriggered.connect(self.setStackedLayout2)

            package.addWidget(toolBar)
            package.addLayout(self.stackedLayout2)
            package.addWidget(subtable)

            widg_ = QWidget()
            widg_.setLayout(package)

            self.tab_widget.addTab(widg_, self.meta_data["additional tab name"])
            self.main_layout.addWidget(self.tab_widget)

    def setStackedLayout2(self, action):
        if action.iconText() == "Manage Data":
            self.stackedLayout2.setCurrentIndex(1)
        
        elif action.iconText() == "Add Data":
            self.stackedLayout2.setCurrentIndex(2)

        elif action.iconText() == "Close":
            self.stackedLayout2.setCurrentIndex(0)

    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

