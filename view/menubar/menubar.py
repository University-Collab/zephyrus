import webbrowser
from PySide2.QtWidgets import QMenuBar, QMenu, QAction
from PySide2.QtGui import QIcon
from view.connect_database.connect_database import ConnectDatabase


class Menubar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connect_db = ConnectDatabase(parent)
        self.init_menubar_menus()

    def init_menubar_menus(self):
        self.menu_icon = QMenu("Logo", self)
        self.logo = QIcon("view/images/branding/zephyrus_transparent.png")
        self.menu_icon.setIcon(self.logo)

        self.file_menu = QMenu("File", self)
        self.edit_menu = QMenu("Edit", self)
        self.database_menu = QMenu("Database", self)
        self.view_menu = QMenu("View", self)
        self.help_menu = QMenu("Help", self)
        self.theme_menu = QMenu("Theme", self.view_menu)

        self.addMenu(self.menu_icon)
        self.addMenu(self.file_menu)
        self.addMenu(self.edit_menu)
        self.addMenu(self.database_menu)
        self.addMenu(self.view_menu)
        self.addMenu(self.help_menu)
        self.view_menu.addMenu(self.theme_menu)

        connect_db_action = QAction(QIcon("view/images/menubar/database-connect.png"), "Connect Database", self)
        connect_db_action.setStatusTip("Connect a new database")
        connect_db_action.triggered.connect(self.connect_db.show)
        self.database_menu.addAction(connect_db_action)

        self.help_menu.addAction("About", self.about_page)

    def about_page(self):
        webbrowser.open("https://university-collab.github.io/zephyrus/")
