from PySide2.QtWidgets import QApplication


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        with open("style_file.qss", "r") as qss_file:
            self.setStyleSheet(qss_file.read())

    def exec(self):
        super().exec_()
