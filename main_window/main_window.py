from PySide2.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Zephyrus - Information Handler")

        