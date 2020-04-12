from PySide2.QtWidgets import QApplication


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.set_dark_theme()

    def exec(self):
        super().exec_()

    def set_dark_theme(self):
        with open("view/dark.qss", "r") as qss_file:
            self.setStyleSheet(qss_file.read())

    def set_light_theme(self):
        with open("view/light.qss", "r") as qss_file:
            self.setStyleSheet(qss_file.read())
