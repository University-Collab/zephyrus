from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QLabel
from PySide2.QtSql import QSqlDatabase
from controller.db_handler.db_handler import DBHandler

class ConnectDatabase(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = None
        self.password = None
        self.db_name = None
        self.host_name = None

    def display_dialog(self):
        self.setWindowTitle("Connect Database")

        self.user_label = QLabel("Database User:")
        self.user = QLineEdit()

        self.pw_label = QLabel("Database Password:")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.db_name_label = QLabel("Database Name:")
        self.db_name = QLineEdit()

        self.host_name_label = QLabel("Host Name:")
        self.host_name = QLineEdit()
        
        self.connect_bttn = QPushButton("Connect")
        self.connect_bttn.clicked.connect(self.connect)

        layout = QGridLayout()
        
        layout.addWidget(self.user_label, 0, 0)
        layout.addWidget(self.user, 0, 1)

        layout.addWidget(self.pw_label, 1, 0)
        layout.addWidget(self.password, 1, 1)

        layout.addWidget(self.db_name_label, 2, 0)
        layout.addWidget(self.db_name, 2, 1)

        layout.addWidget(self.host_name_label, 3, 0)
        layout.addWidget(self.host_name, 3, 1)

        layout.addWidget(self.connect_bttn, 4, 1)

        self.setLayout(layout)
        self.setModal(True)

        self.show()

    def connect(self):
        # Just for testing
        print(
            f'User: {self.user.text()}\nPassword: {self.password.text()}\nDB name: {self.db_name.text()}\nHost Name: {self.host_name.text()}'
        )

        """
        Implement using 'QSqlDatabase' PySide2 module
        """
