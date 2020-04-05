from PySide2.QtWidgets import QMenuBar, QMenu
from PySide2.QtGui import QIcon


class Menubar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_menubar_menus()

    def init_menubar_menus(self):
        self.menu_icon = QMenu("Logo", self)
        self.logo = QIcon("./images/logo/menu_bar_logo.png")
        self.menu_icon.setIcon(self.logo)

        self.file_menu = QMenu("File", self)
        self.edit_menu = QMenu("Edit", self)
        self.tools_menu = QMenu("Tools", self)
        self.view_menu = QMenu("View", self)
        self.help_menu = QMenu("Help", self)

        self.addMenu(self.menu_icon)
        self.addMenu(self.file_menu)
        self.addMenu(self.edit_menu)
        self.addMenu(self.tools_menu)
        self.addMenu(self.view_menu)
        self.addMenu(self.help_menu)
