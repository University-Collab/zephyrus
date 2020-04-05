from PySide2.QtWidgets import QWidget, QTabWidget
from PySide2.QtGui import QIcon, Qt

class CentralWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.remove_tab)
        # self.setStyleSheet("background-color: #212121; border: solid 1px #1a1a1a;")
        self.setMovable(True)


    
    def add_tab(self, widget, icon, label):
        # widget.setStyleSheet("background-color: #1a1a1a")
        self.addTab(widget, icon, label)

    def remove_tab(self, index):
        self.removeTab(index)