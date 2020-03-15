from PySide2.QtWidgets import QDockWidget


class Dock(QDockWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent=parent)
