from sys import platform
from PySide2.QtWidgets import QApplication


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        if platform == "linux" or platform == "darwin":  # darwin == macOS
            with open("view/style_linux.qss", "r") as qss_file:
                self.setStyleSheet(qss_file.read())
        else:
            # add style for Windows
            pass

    def exec(self):
        super().exec_()
