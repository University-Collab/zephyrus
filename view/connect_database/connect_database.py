import pickle, os
import pymysql as mysql
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QLabel, QMessageBox

class ConnectDatabase(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowTitle("Connect Database")

        self.user_label = QLabel("Database User:")
        self.user = QLineEdit()
        self.user.setPlaceholderText("e.g. root")
        self.user.setDragEnabled(True)
        self.user.setFocus()
        self.user.setClearButtonEnabled(True)

        self.pw_label = QLabel("Database Password:")
        self.password = QLineEdit()
        self.password.setPlaceholderText("e.g. toor")
        self.password.setClearButtonEnabled(True)
        self.password.setEchoMode(QLineEdit.Password)

        self.db_name_label = QLabel("Database Name:")
        self.db_name = QLineEdit()
        self.db_name.setPlaceholderText("e.g. bank-db")
        self.db_name.setDragEnabled(True)
        self.db_name.setClearButtonEnabled(True)

        self.host_name_label = QLabel("Host Name:")
        self.host_name = QLineEdit()
        self.host_name.setPlaceholderText("e.g. localhost")
        self.host_name.setDragEnabled(True)
        self.host_name.setClearButtonEnabled(True)
        
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

    def connect(self):
        if os.path.exists("model/session/connected_dbs"):
            with open("model/session/connected_dbs", "rb") as sessions:
                db_sessions = pickle.load(sessions)
        else:
            db_sessions = []

        is_connected = False
        
        for db in db_sessions:
            if db["db"] == self.db_name.text():
                is_connected = True
                QMessageBox.critical(self, "Database Already Connected", "Database with the same name is already connected.", QMessageBox.Close)
                break

        if not is_connected:
            if len(self.user.text()) > 0 and len(self.password.text()) > 0 and len(self.db_name.text()) > 0 and len(self.host_name.text()) > 0:
                connection = mysql.connect(
                        host=self.host_name.text(),
                        user=self.user.text(),
                        password=self.password.text(),
                        db=self.db_name.text(),
                        charset="utf8mb4",
                        cursorclass=mysql.cursors.DictCursor
                    )
                try:
                    db_sessions.append(
                        {
                            "index": len(db_sessions) + 1,
                            "host": self.host_name.text(),
                            "user": self.user.text(),
                            "password": self.password.text(),
                            "db": self.db_name.text()
                        }
                    )

                    QMessageBox.information(self, "Database connected. You rock!", "Hooray! Database successfully connected with Zephyrus.\n\nHint: Press Ctrl+R to refresh databases", QMessageBox.Ok)

                    with open("model/session/connected_dbs", "wb") as sessions:
                        pickle.dump(db_sessions, sessions)

                    self.close()

                except mysql.Error as e:
                    print(f'\nDB Error: {e.args[1]}\n')
                    QMessageBox.critical(self, "Warning", "Wrong database credentials, you might be bad at typing...", QMessageBox.Close)
                finally:
                    connection.close()
            else:
                QMessageBox.critical(self, "Warning", "You didn't fill out all fields!", QMessageBox.Close)