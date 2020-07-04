from PySide2.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QStackedLayout, QTabWidget,
                               QTableView, QAbstractItemView, QLineEdit, QMenu,
                               QAction, QSizePolicy, QLineEdit, QComboBox, QListWidget, QToolBar, QMessageBox, QLayout, QBoxLayout)
from PySide2 import QtGui
from PySide2.QtGui import QIcon

from controller.db_handler.db_handler import DBHandler
from model.table_model.db_table_model import DBTableModel
from view.table_view.db_table_view import DBTableView
from view.section_add_data.db_add_data import DBAddData
from view.section_manage_data.db_manage_data import DBManageData

class DBWorkspace(QWidget):
    def __init__(self, db, table, parent=None):
        super().__init__(parent)
        
        self.main_layout = QVBoxLayout()
        self.tab_widget = None
        self.handler = None
        self.db = db
        self.table = table
        self.table_model = None
        self.create_tab_widget()

        self.main_table = DBTableView(self.tab_widget)
        self.main_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.main_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.init_table()
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
        
        self.manageData = DBManageData(self.main_table)
        self.addData = DBAddData(self.main_table)

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

    def row_selected(self, index):
        if index.column() == len(self.main_table.model().columns):

            model = self.main_table.model()
            selected_data = model.get_element(index)

            self.selected_row = index.row()

    def create_tab_widget(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_tab)
    
    def delete_tab(self, index):
        self.tab_widget.removeTab(index)

    def init_table(self):
        self.handler = DBHandler(self.db, self.table, self)
        self.table_model = DBTableModel(self.handler)
        self.main_table.setModel(self.table_model)

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

