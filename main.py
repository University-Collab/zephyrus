import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QAction
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
    dock.tree_init()
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)
    toggle_dock_action = dock.toggleViewAction()
    toggle_dock_action.setShortcut("Ctrl+B")
    menubar.view_menu.addAction(toggle_dock_action)

    dock_db = Dock("Connected Databases", central_widget, window)
    dock_db.init_db_tree()
    window.addDockWidget(Qt.LeftDockWidgetArea, dock_db)
    toggle_connected_dbs_action = dock_db.toggleViewAction()
    toggle_connected_dbs_action.setShortcut("Ctrl+D")
    
    refresh_action = QAction(QIcon("view/images/menubar/refresh.png"), "Refresh Connected DBs", dock_db)
    refresh_action.setShortcut("Ctrl+R")
    refresh_action.setStatusTip("Refreshes list of connected databases in the dock")
    refresh_action.triggered.connect(dock_db.connected_dbs)
    
    menubar.tools_menu.addAction(refresh_action)
    menubar.view_menu.addAction(toggle_connected_dbs_action)

    window.showMaximized()

    sys.exit(app.exec())
