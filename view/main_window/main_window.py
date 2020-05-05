from PySide2.QtWidgets import QMainWindow, QMessageBox
from PySide2.QtGui import QIcon
from PySide2.QtCore import QEvent


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Zephyrus - Information Handler")
        self.setWindowIcon(QIcon("view/images/branding/zephyrus_transparent.png"))

    def closeEvent(self, event):
        close_prompt = QMessageBox()
        close_prompt.setWindowTitle("Exit Zephyrus")
        close_prompt.setText("Are you sure you want to exit Zephyrus?")
        close_prompt.setStandardButtons(QMessageBox.Close | QMessageBox.Yes)
        close_prompt.setDefaultButton(QMessageBox.Close)
        close_prompt.setIcon(QMessageBox.Question)

        ret = close_prompt.exec_()

        if ret == QMessageBox.Close:
            event.ignore()
            return
        elif ret == QMessageBox.Yes:
            event.accept()
