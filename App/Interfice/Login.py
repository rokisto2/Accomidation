import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from App.transferDesign.ui_login import Ui_MainWindow # Импортируйте сгенерированный файл напрямую

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключите кнопку входа к методу handle_login
        self.ui.loginButton.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.mail.text()
        password = self.ui.password.text()
        role = "student"
        if self.ui.radioStudent.isChecked():
            role = "student"
        elif self.ui.radioAdministration.isChecked():
            role = "administrator"
        elif self.ui.radioDeaneryStaff.isChecked():
            role = "deanery_staff"


        response = requests.post("http://localhost:8000/api/auth/token", data={"username": username, "password": password, "scope": role})

        if response.status_code == 200:
            QMessageBox.information(self, "Login Successful", "Welcome!")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())