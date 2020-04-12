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
    menubar.theme_menu.addAction("Dark", app.set_dark_theme)
    menubar.theme_menu.addSeparator()
    menubar.view_menu.addSeparator()
    menubar.theme_menu.addAction("Light", app.set_light_theme)
    window.setMenuBar(menubar)

    toolbar = Toolbar("Tool Bar", window)
    toggle_toolbar_action = toolbar.toggleViewAction()
    toggle_toolbar_action.setShortcut("Ctrl+T")
    menubar.view_menu.addAction(toggle_toolbar_action)
    window.addToolBar(Qt.LeftToolBarArea, toolbar)

    central_widget = CentralWidget(window)
    window.setCentralWidget(central_widget)

    status_bar = StatusBar(window)
    window.setStatusBar(status_bar)

    dock = Dock("File Explorer", central_widget, window)
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)
    toggle_dock_action = dock.toggleViewAction()
    toggle_dock_action.setShortcut("Ctrl+B")
    menubar.view_menu.addAction(toggle_dock_action)

    window.showMaximized()

    sys.exit(app.exec())
