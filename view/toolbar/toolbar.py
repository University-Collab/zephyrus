from PySide2.QtWidgets import QToolBar, QWidget, QToolButton
from PySide2.QtGui import QIcon


class Toolbar(QToolBar):
    def __init__(self, title=None, parent=None):
        QToolBar.__init__(self, title, parent)
        self.init_toolbar_buttons()

    def init_toolbar_buttons(self):
        self.connect_database = QToolButton(self)
        self.connect_database.setIcon(QIcon("view/images/toolbar/database-connect.png"))
        self.connect_database.setToolTip("Connect Database")
        self.addWidget(self.connect_database)

        self.open = QToolButton(self)
        self.open.setIcon(QIcon("view/images/toolbar/open.png"))
        self.open.setToolTip("Open File")
        self.addWidget(self.open)

        self.save = QToolButton(self)
        self.save.setIcon(QIcon("view/images/toolbar/save.png"))
        self.save.setToolTip("Save")
        self.addWidget(self.save)

        self.search = QToolButton(self)
        self.search.setIcon(QIcon("view/images/toolbar/search.png"))
        self.search.setToolTip("Search")
        self.addWidget(self.search)
