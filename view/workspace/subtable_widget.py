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

class SubtableWidget(QWidget):
    def __init__(self, subtable, parent=None):
        super().__init__(parent)
        self.subtable = subtable
        self.subtable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.subtable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.subtable.clicked.connect(self.row_selected)
        self.selected_row = 0


        self.package = QVBoxLayout()

        self.toolBar = QToolBar()
        self.toolBar.setMovable(True)

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
        
        self.toolBar.addAction(QIcon("view/images/toolbar/list_48px.png"), "Manage Data")
        self.toolBar.addAction(QIcon("view/images/toolbar/add_new_40px.png"), "Add Data")
        self.toolBar.addAction(sub_first)
        self.toolBar.addAction(sub_up)
        self.toolBar.addAction(sub_down)
        self.toolBar.addAction(sub_last)
        self.toolBar.addAction(QIcon("view/images/toolbar/close_window_26px.png"), "Close")

        self.manageData2 = ManageData(self.subtable)

        self.addData2 = AddData(self.subtable)
        self.label = QLabel()
        self.label.setText("Work with data, choose state.")

        self.stacked_layout_2 = QVBoxLayout()
        self.stacked_layout_2.addStretch(0)
        # self.stacked_layout_2.addWidget(self.label)
        # self.stacked_layout_2.addWidget(self.manageData2)
        # self.stacked_layout_2.addWidget(self.addData2)
        # self.stacked_layout_2.setCurrentIndex(0)

        self.toolBar.actionTriggered.connect(self.sub_toolbar_actions)

        self.package.addWidget(self.toolBar)
        self.package.addLayout(self.stacked_layout_2)
        self.package.addWidget(self.subtable)

        self.setLayout(self.package)

    def sub_toolbar_actions(self, action):
        if action.iconText() == "Manage Data":
            if self.stacked_layout_2.indexOf(self.addData2) == -1 and self.stacked_layout_2.indexOf(self.manageData2) == -1 and self.stacked_layout_2.indexOf(self.label) == -1:
                self.stacked_layout_2.addWidget(self.manageData2)
                self.manageData2.setVisible(True)
                return
            if self.stacked_layout_2.indexOf(self.addData2) != -1:
                self.stacked_layout_2.removeWidget(self.addData2)
                self.addData2.setVisible(False)
                self.stacked_layout_2.addWidget(self.manageData2)
                self.manageData2.setVisible(True)
                return
            if self.stacked_layout_2.indexOf(self.label) != -1:
                self.stacked_layout_2.removeWidget(self.label)
                self.label.setVisible(False)
                self.stacked_layout_2.addWidget(self.manageData2)
                self.manageData2.setVisible(True)
                return
            return 
            
        
        elif action.iconText() == "Add Data":
            if self.stacked_layout_2.indexOf(self.addData2) == -1 and self.stacked_layout_2.indexOf(self.manageData2) == -1 and self.stacked_layout_2.indexOf(self.label) == -1:
                self.stacked_layout_2.addWidget(self.addData2)
                self.addData2.setVisible(True)
                return
            if self.stacked_layout_2.indexOf(self.manageData2) != -1:
                self.stacked_layout_2.removeWidget(self.manageData2)
                self.manageData2.setVisible(False)
                self.stacked_layout_2.addWidget(self.addData2)
                self.addData2.setVisible(True)
                return
            if self.stacked_layout_2.indexOf(self.label) != -1:
                self.stacked_layout_2.removeWidget(self.label)
                self.label.setVisible(False)
                self.stacked_layout_2.addWidget(self.addData2)
                self.addData2.setVisible(True)
                return
            return
            

        elif action.iconText() == "Close":
            if self.stacked_layout_2.indexOf(self.addData2) == -1 and self.stacked_layout_2.indexOf(self.manageData2) == -1 and self.stacked_layout_2.indexOf(self.label) == -1:
                self.stacked_layout_2.addWidget(self.label)
                self.label.setVisible(True)
                return
            if self.stacked_layout_2.indexOf(self.addData2) != -1:
                self.stacked_layout_2.removeWidget(self.addData2)
                self.addData2.setVisible(False)
                self.stacked_layout_2.addWidget(self.label)
                self.label.setVisible(True)
                return
            if self.stacked_layout_2.indexOf(self.manageData2) != -1:
                self.stacked_layout_2.removeWidget(self.manageData2)
                self.manageData2.setVisible(False)
                self.stacked_layout_2.addWidget(self.label)
                self.label.setVisible(True)
                return
            return

    def row_selected(self, index):
        self.selected_row = index.row()

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