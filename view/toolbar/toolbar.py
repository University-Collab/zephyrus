from PySide2.QtWidgets import QToolBar, QWidget, QToolButton
from PySide2.QtGui import QIcon
from view.connect_database.connect_database import ConnectDatabase


class Toolbar(QToolBar):
    def __init__(self, title=None, parent=None):
        QToolBar.__init__(self, title, parent)
        self.connect_db = ConnectDatabase(parent)
        self.init_toolbar_buttons()

    def init_toolbar_buttons(self):
        self.connect_database = QToolButton(self)
        self.connect_database.setIcon(QIcon("view/images/toolbar/database-connect.png"))
        self.connect_database.setToolTip("Connect Database")
        self.connect_database.clicked.connect(self.connect_db.display_dialog)
        self.addWidget(self.connect_database)

        self.open = QToolButton(self)
        self.open.setIcon(QIcon("view/images/toolbar/open.png"))
        self.open.setToolTip("Open File")
        self.addWidget(self.open)
