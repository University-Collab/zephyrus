import json, pickle
from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QLineEdit, QComboBox, QListWidget, QToolBar, QMessageBox, QLayout, QBoxLayout)
                               
from PySide2 import QtGui
from PySide2.QtGui import QIcon

from controller.serial_data_handler.serial_data_handler import SerialDataHandler
from controller.sequential_data_handler.sequential_data_handler import (
    SequentialDataHandler, )
from model.table_model.table_model import TableModel
from view.table_view.table_view import TableView
from view.section_manage_data.manage_data import ManageData
from view.section_add_data.add_data import AddData
from view.workspace.subtable_widget import SubtableWidget


class Workspace(QWidget):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout()
        self.main_layout.setDirection(QBoxLayout.TopToBottom)
        self.tab_widget = QTabWidget()
        self.file_path = file_path
        self.meta_path = None
        self.subtable_meta_path = None
        self.subtable_path = None
        self.handler_type = None
        self.handler = None
        self.table_model = None
        self.meta_data = None
        self.sub_meta_data = None
        self.create_tab_widget()

        self.main_table = TableView(self.tab_widget)
        self.main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.create_model()
        self.main_table.clicked.connect(self.row_selected)

        self.package = QVBoxLayout()
        self.package.addStretch(1)
        
        self.toolBar = QToolBar()
        self.toolBar.setMovable(True)

        self.up = QAction(QIcon("view/images/toolbar/baseline_expand_less_black_48dp.png"), "Up", self.main_table)
        self.up.setStatusTip("Move one up")
        self.up.triggered.connect(self.jump_up)

        self.down = QAction(QIcon("view/images/toolbar/baseline_expand_more_black_48dp.png"), "Down", self.main_table)
        self.down.setStatusTip("Move one down")
        self.down.triggered.connect(self.jump_down)

        self.first = QAction(QIcon("view/images/toolbar/baseline_first_page_black_48dp.png"), "Jump to first", self.main_table)
        self.first.setStatusTip("Jump to first")
        self.first.triggered.connect(self.jump_to_first)

        self.last = QAction(QIcon("view/images/toolbar/baseline_last_page_black_48dp.png"), "Jump to last", self.main_table)
        self.last.setStatusTip("Jump to last")
        self.last.triggered.connect(self.jump_to_last)
        
        self.toolBar.addAction(QIcon("view/images/toolbar/list_48px.png"), "Manage Data")
        self.toolBar.addAction(QIcon("view/images/toolbar/add_new_40px.png"), "Add Data")
        self.toolBar.addAction(self.first)
        self.toolBar.addAction(self.up)
        self.toolBar.addAction(self.down)
        self.toolBar.addAction(self.last)
        self.toolBar.addAction(QIcon("view/images/toolbar/close_window_26px.png"), "Close")

        self.manageData = ManageData(self.main_table)
        self.addData = AddData(self.main_table)

        self.stacked_layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText("Work with data, choose state.")
        
        self.toolBar.actionTriggered.connect(self.toolbar_actions)

        self.package.addWidget(self.toolBar)
        self.package.addLayout(self.stacked_layout)
        self.package.addWidget(self.main_table)
        
        self.main_layout.addLayout(self.package)

        self.selected_row = 0

        self.main_layout.addStretch(2)
        self.setLayout(self.main_layout)

    def toolbar_actions(self, action):
        if action.iconText() == "Manage Data":
            if self.stacked_layout.indexOf(self.addData) == -1 and self.stacked_layout.indexOf(self.manageData) == -1 and self.stacked_layout.indexOf(self.label) == -1:
                self.stacked_layout.addWidget(self.manageData)
                self.manageData.setVisible(True)
                return
            if self.stacked_layout.indexOf(self.addData) != -1:
                self.stacked_layout.removeWidget(self.addData)
                self.addData.setVisible(False)
                self.stacked_layout.addWidget(self.manageData)
                self.manageData.setVisible(True)
                return
            if self.stacked_layout.indexOf(self.label) != -1:
                self.stacked_layout.removeWidget(self.label)
                self.label.setVisible(False)
                self.stacked_layout.addWidget(self.manageData)
                self.manageData.setVisible(True)
                return
            return 
            
        
        elif action.iconText() == "Add Data":
            if self.stacked_layout.indexOf(self.addData) == -1 and self.stacked_layout.indexOf(self.manageData) == -1 and self.stacked_layout.indexOf(self.label) == -1:
                self.stacked_layout.addWidget(self.addData)
                self.addData.setVisible(True)
                return
            if self.stacked_layout.indexOf(self.manageData) != -1:
                self.stacked_layout.removeWidget(self.manageData)
                self.manageData.setVisible(False)
                self.stacked_layout.addWidget(self.addData)
                self.addData.setVisible(True)
                return
            if self.stacked_layout.indexOf(self.label) != -1:
                self.stacked_layout.removeWidget(self.label)
                self.label.setVisible(False)
                self.stacked_layout.addWidget(self.addData)
                self.addData.setVisible(True)
                return
            return
            

        elif action.iconText() == "Close":
            if self.stacked_layout.indexOf(self.addData) == -1 and self.stacked_layout.indexOf(self.manageData) == -1 and self.stacked_layout.indexOf(self.label) == -1:
                self.stacked_layout.addWidget(self.label)
                self.label.setVisible(True)
                return
            if self.stacked_layout.indexOf(self.addData) != -1:
                self.stacked_layout.removeWidget(self.addData)
                self.addData.setVisible(False)
                self.stacked_layout.addWidget(self.label)
                self.label.setVisible(True)
                return
            if self.stacked_layout.indexOf(self.manageData) != -1:
                self.stacked_layout.removeWidget(self.manageData)
                self.manageData.setVisible(False)
                self.stacked_layout.addWidget(self.label)
                self.label.setVisible(True)
                return
            return
               

    def set_paths(self):
        subtable_path = self.file_path.split("storage/")[0] + "storage/" + self.meta_data["linked file"]
        subtable_meta_path = self.file_path.split("storage/")[0] + "meta/" + self.meta_data["linked file"] + "_metadata.json"
        with open(subtable_meta_path, "r") as data:
            sub_meta_data = json.load(data)
            info = []
            info.append(subtable_path)
            info.append(subtable_meta_path) 
            info.append(sub_meta_data)
            return info

    def create_model(self): 
        temp = self.file_path.split("storage/")
        self.meta_path = temp[0] + "meta/" + temp[1].split(
            ".")[0] + "_metadata.json"
        with open(self.meta_path) as metadata:
            data = json.load(metadata)
            self.meta_data = data


        if self.meta_data["handler type"] == "serial":
            self.handler = SerialDataHandler(self.file_path, self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

        if self.meta_data["handler type"] == "sequential":
            self.handler = SequentialDataHandler(self.file_path,
                                                self.meta_path)
            self.table_model = TableModel(self.handler)
            self.main_table.setModel(self.table_model)

    def row_selected(self, index):
        if index.column() == len(self.main_table.model().metadata["columns"]):

            model = self.main_table.model()
            selected_data = model.get_element(index)

            self.selected_row = index.row()

            info = self.set_paths()
            unique_data = selected_data[self.meta_data["search key"]] 

            sub_meta_data = info[2]
            subtable_path = info[0]
            subtable_meta_path = info[1]         

            if sub_meta_data["handler type"] == "serial":
                subtable_model = TableModel(
                    SerialDataHandler(subtable_path, subtable_meta_path,
                                    unique_data))

            if sub_meta_data["handler type"] == "sequential":
                subtable_model = TableModel(
                    SequentialDataHandler(subtable_path, subtable_meta_path,
                                        unique_data))

            subtable = TableView(self.tab_widget)
            subtable.setModel(subtable_model)

            subtable_widget = SubtableWidget(subtable)

            self.tab_widget.addTab(subtable_widget, self.meta_data["additional tab name"])
            self.main_layout.addWidget(self.tab_widget)


    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)

    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    """
    Table navigation jumps
    """
    def jump_up(self):
        if self.selected_row != 0:
            self.selected_row -= 1
            self.main_table.selectRow(self.selected_row)

    def jump_down(self):
        if self.selected_row < len(self.main_table.model().displayed_d) - 1:
            self.selected_row += 1
            self.main_table.selectRow(self.selected_row)

    def jump_to_first(self):
        self.selected_row = 0
        self.main_table.selectRow(self.selected_row)

    def jump_to_last(self):
        self.selected_row = len(self.main_table.model().displayed_d) - 1
        self.main_table.selectRow(self.selected_row)


