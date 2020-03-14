import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import Qt

from application.application import Application
from main_window.main_window import MainWindow
from toolbar.toolbar import Toolbar
from status_bar.status_bar import StatusBar
from menubar.menubar import Menubar


if __name__ == "__main__":
    app = Application(sys.argv)

    window = MainWindow() 
    window.resize(800, 600)

    menubar = Menubar(window)
    window.setMenuBar(menubar)

    toolbar = Toolbar(window)
    window.addToolBar(Qt.LeftToolBarArea, toolbar)

    status_bar = StatusBar(window)
    window.setStatusBar(status_bar)

    window.show()

    sys.exit(app.exec())
