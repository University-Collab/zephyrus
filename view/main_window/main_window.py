from PySide2.QtWidgets import QMainWindow
from PySide2.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Zephyrus - Information Handler")
        self.setWindowIcon(QIcon("view/images/branding/zephyrus_transparent.png"))
