import webbrowser
from PySide2.QtWidgets import QMenuBar, QMenu
from PySide2.QtGui import QIcon


class Menubar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

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

        self.help_menu.addAction("About", self.about_page)

    def about_page(self):
        webbrowser.open("https://university-collab.github.io/zephyrus/")
