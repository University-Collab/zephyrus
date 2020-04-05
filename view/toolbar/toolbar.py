from PySide2.QtWidgets import QToolBar, QWidget, QToolButton
from PySide2.QtGui import QIcon


class Toolbar(QToolBar):
    def __init__(self, title=None, parent=None):
        QToolBar.__init__(self, title, parent)
        self.init_toolbar_buttons()

    def init_toolbar_buttons(self):
        self.create_new = QToolButton(self)
        self.create_new.setIcon(QIcon("view/images/toolbar/create_new.png"))
        self.addWidget(self.create_new)

        self.open = QToolButton(self)
        self.open.setIcon(QIcon("view/images/toolbar/open.png"))
        self.addWidget(self.open)

        self.save = QToolButton(self)
        self.save.setIcon(QIcon("view/images/toolbar/save.png"))
        self.addWidget(self.save)

        self.search = QToolButton(self)
        self.search.setIcon(QIcon("view/images/toolbar/search.png"))
        self.addWidget(self.search)

        self.undo = QToolButton(self)
        self.undo.setIcon(QIcon("view/images/toolbar/undo.png"))
        self.addWidget(self.undo)

        self.redo = QToolButton(self)
        self.redo.setIcon(QIcon("view/images/toolbar/redo.png"))
        self.addWidget(self.redo)
