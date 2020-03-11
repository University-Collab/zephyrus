import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import Qt

from toolbar.toolbar import Toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Zephyrus - Information Handler")

        with open("style_file.qss", "r") as qss_file:
            self.setStyleSheet(qss_file.read())

        self.menu = self.menuBar()

        self.file_menu = self.menu.addMenu("File")
        self.edit_menu = self.menu.addMenu("Edit")
        self.tools_menu = self.menu.addMenu("Tools")
        self.view_menu = self.menu.addMenu("View")
        self.help_menu = self.menu.addMenu("Help")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)

    toolbar = Toolbar("Hello world", window)
    window.addToolBar(Qt.LeftToolBarArea, toolbar)

    window.show()

    sys.exit(app.exec_())
