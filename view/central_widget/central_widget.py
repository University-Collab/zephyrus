from PySide2.QtWidgets import QWidget, QTabWidget
from PySide2.QtGui import QIcon, Qt


class CentralWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.remove_tab)
        self.setMovable(True)

    def add_tab(self, widget, icon, label):
        self.addTab(widget, icon, label)

    def remove_tab(self, index):
        self.removeTab(index)
