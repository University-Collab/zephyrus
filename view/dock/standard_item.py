from PySide2.QtGui import QStandardItem, QFont

class StandardItem(QStandardItem):
    def __init__(self, text, font_size=12, is_bold=False):
        super().__init__()

        font = QFont('Open Sans', font_size)
        font.setBold(is_bold)

        self.setEditable(False)
        self.setFont(font)
        self.setText(text)