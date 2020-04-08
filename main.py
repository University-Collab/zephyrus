import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

from view.application.application import Application
from view.main_window.main_window import MainWindow
from view.toolbar.toolbar import Toolbar
from view.status_bar.status_bar import StatusBar
from view.menubar.menubar import Menubar
from view.dock.dock import Dock
from view.central_widget.central_widget import CentralWidget
from view.workspace.workspace import Workspace

if __name__ == "__main__":
    app = Application(sys.argv)

    window = MainWindow()

    menubar = Menubar(window)
    window.setMenuBar(menubar)

    toolbar = Toolbar(window)
    window.addToolBar(Qt.LeftToolBarArea, toolbar)

    central_widget = CentralWidget(window)
    window.setCentralWidget(central_widget)

    status_bar = StatusBar(window)
    window.setStatusBar(status_bar)

    dock = Dock("File Explorer", central_widget, window)
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)
    toggle_dock_action = dock.toggleViewAction()
    menubar.view_menu.addAction(toggle_dock_action)

    window.showMaximized()

    sys.exit(app.exec())
