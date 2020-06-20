from PySide2.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.showMessage("Have a productive day! -Zephyrus", 0)
