import pickle, os
import pymysql as mysql
from PySide2.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QLabel, QMessageBox

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
        if os.path.getsize("model/session/connected_dbs") > 0:
            with open("model/session/connected_dbs", "rb") as sessions:
                db_sessions = pickle.load(sessions)
        else:
            db_sessions = []

        is_connected = False
        
        for db in db_sessions:
            if db["db"] == self.db_name.text():
                is_connected = True

                err_mssg = QMessageBox(self)
                err_mssg.setText("Database with the same name is already connected.")
                err_mssg.setStandardButtons(QMessageBox.Close)
                err_mssg.setIcon(QMessageBox.Critical)
                err_mssg.setWindowTitle("Database Already Connected")
                err_mssg.setModal(True)
                err_mssg.exec()

                break

        if not is_connected:
            try:
                connection = mysql.connect(
                    host=self.host_name.text(),
                    user=self.user.text(),
                    password=self.password.text(),
                    db=self.db_name.text(),
                    charset="utf8mb4",
                    cursorclass=mysql.cursors.DictCursor
                )

                db_sessions.append(
                    {
                        "index": len(db_sessions) + 1,
                        "host": self.host_name.text(),
                        "user": self.user.text(),
                        "password": self.password.text(),
                        "db": self.db_name.text()
                    }
                )

                connected_mssg = QMessageBox(self)
                connected_mssg.setText("Hooray! Database successfully connected with Zephyrus.")
                connected_mssg.setStandardButtons(QMessageBox.Ok)
                connected_mssg.setIcon(QMessageBox.Information)
                connected_mssg.setWindowTitle("Database connected. You rock!")
                connected_mssg.setModal(True)
                connected_mssg.exec()

                with open("model/session/connected_dbs", "wb") as sessions:
                    pickle.dump(db_sessions, sessions)

                self.close()

            except mysql.Error as e:
                print(f'\nDB Error: {e.args[1]}\n')
                err_mssg = QMessageBox(self)
                err_mssg.setText("Wrong database credentials, you might be bad at typing...")
                err_mssg.setStandardButtons(QMessageBox.Close)
                err_mssg.setIcon(QMessageBox.Critical)
                err_mssg.setWindowTitle("Database Error")
                err_mssg.setModal(True)
                err_mssg.exec()
            
            finally:
                connection.close()