from PySide2.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        """
        Added so that something shows up in the status bar
        *** Remove after adding status bar functionality ***
        """
        self.showMessage("Status bar has been set", 0)
