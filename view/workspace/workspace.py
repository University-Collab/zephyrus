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

        self.stacked_layout = QStackedLayout()
        self.label = QLabel()
        self.label.setText("Work with data, choose state.")
        self.stacked_layout.addWidget(self.label)
        self.stacked_layout.addWidget(self.manageData)
        self.stacked_layout.addWidget(self.addData)
        self.stacked_layout.setCurrentIndex(0)

        self.toolBar.actionTriggered.connect(self.toolbar_actions)

        self.package.addWidget(self.toolBar)
        self.package.addLayout(self.stacked_layout)
        self.package.addWidget(self.main_table)
        
        self.main_layout.addLayout(self.package)

        self.selected_row = 0
     
        self.setLayout(self.main_layout)

    def toolbar_actions(self, action):
        if action.iconText() == "Manage Data":
            self.stacked_layout.setCurrentIndex(1)
        
        elif action.iconText() == "Add Data":
            self.stacked_layout.setCurrentIndex(2)

        elif action.iconText() == "Close":
            self.stacked_layout.setCurrentIndex(0)    

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
        if index.column() <= len(self.main_table.model().metadata["columns"]):

            model = self.main_table.model()
            selected_data = model.get_element(index)

            self.selected_row = index.row()

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

            self.subtable = TableView(self.tab_widget)
            self.subtable.setModel(subtable_model)

            package = QVBoxLayout()

            toolBar = QToolBar()
            toolBar.setMovable(True)

            sub_up = QAction(QIcon("view/images/toolbar/baseline_expand_less_black_48dp.png"), "Up", self.subtable)
            sub_up.setStatusTip("Move one up")
            sub_up.triggered.connect(self.sub_up)

            sub_down = QAction(QIcon("view/images/toolbar/baseline_expand_more_black_48dp.png"), "Down", self.subtable)
            sub_down.setStatusTip("Move one down")
            sub_down.triggered.connect(self.sub_down)

            sub_first = QAction(QIcon("view/images/toolbar/baseline_first_page_black_48dp.png"), "Jump to first", self.subtable)
            sub_first.setStatusTip("Jump to first")
            sub_first.triggered.connect(self.sub_first)

            sub_last = QAction(QIcon("view/images/toolbar/baseline_last_page_black_48dp.png"), "Jump to last", self.subtable)
            sub_last.setStatusTip("Jump to last")
            sub_last.triggered.connect(self.sub_last)
            
            toolBar.addAction(QIcon("view/images/toolbar/list_48px.png"), "Manage Data")
            toolBar.addAction(QIcon("view/images/toolbar/add_new_40px.png"), "Add Data")
            toolBar.addAction(sub_first)
            toolBar.addAction(sub_up)
            toolBar.addAction(sub_down)
            toolBar.addAction(sub_last)
            toolBar.addAction(QIcon("view/images/toolbar/close_window_26px.png"), "Close")

            manageData = ManageData(self.subtable)

            addData = AddData(self.subtable)

            self.stacked_layout_2 = QStackedLayout()
            self.stacked_layout_2.addWidget(self.label)
            self.stacked_layout_2.addWidget(manageData)
            self.stacked_layout_2.addWidget(addData)
            self.stacked_layout_2.setCurrentIndex(0)

            toolBar.actionTriggered.connect(self.sub_toolbar_actions)

            package.addWidget(toolBar)
            package.addLayout(self.stacked_layout_2)
            package.addWidget(self.subtable)

            widg_ = QWidget()
            widg_.setLayout(package)

            self.tab_widget.addTab(widg_, self.meta_data["additional tab name"])
            self.main_layout.addWidget(self.tab_widget)

    def sub_toolbar_actions(self, action):
        if action.iconText() == "Manage Data":
            self.stacked_layout_2.setCurrentIndex(1)
        
        elif action.iconText() == "Add Data":
            self.stacked_layout_2.setCurrentIndex(2)

        elif action.iconText() == "Close":
            self.stacked_layout_2.setCurrentIndex(0)

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

    def sub_up(self):
        if self.selected_row != 0:
            self.selected_row -= 1
            self.subtable.selectRow(self.selected_row)

    def sub_down(self):
        if self.selected_row < len(self.subtable.model().displayed_d) - 1:
            self.selected_row += 1
            self.subtable.selectRow(self.selected_row)

    def sub_first(self):
        self.selected_row = 0
        self.subtable.selectRow(self.selected_row)

    def sub_last(self):
        self.selected_row = len(self.subtable.model().displayed_d) - 1
        self.subtable.selectRow(self.selected_row)

