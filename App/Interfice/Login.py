import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

import jwt

from App.Interfice.main import AdministratorMainWindow
from App.Interfice.student_info_window import StudentInfoWindow
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
            token = response.json()["access_token"]
            decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
            if role == "student":
                decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
                student_id = decoded_token.get("user_id")
                self.student_info_window = StudentInfoWindow(token, student_id)
                self.student_info_window.show()
            elif role == "deanery_staff":
                from App.Interfice.DeaneryStaffMainWindow import DeaneryStaffMainWindow
                self.DeaneryStaffMainWindow = DeaneryStaffMainWindow(token)
                self.DeaneryStaffMainWindow.show()
            elif role == "administrator":
                admin_response = requests.get(f"http://localhost:8000/api/administration/{user_id}",
                                              headers={"Authorization": f"Bearer {token}"})
                if admin_response.status_code == 200:
                    dormitory_id = admin_response.json().get("dormitory_id")
                    self.administrator_main_window = AdministratorMainWindow(token, dormitory_id)
                    self.administrator_main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())