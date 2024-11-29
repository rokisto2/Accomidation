from PySide6.QtGui import QAction, QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
import requests

class StudentInfoWindow(QMainWindow):
    def __init__(self, token, student_id):
        super().__init__()

        font = QFont("Courier", 14)  # Моноширинный шрифт с размером 14
        self.setFont(font)

        self.setup_menu()
        self.len_violations_table = None
        self.token = token
        self.student_id = student_id

        self.setWindowTitle("Student Information")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.student_info_label = QLabel("Student Information")
        layout.addWidget(self.student_info_label)

        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(2)
        self.violations_table.setHorizontalHeaderLabels(["Description", "Date"])
        self.violations_table.setSortingEnabled(True)  # Enable sorting

        layout.addWidget(self.violations_table)

        central_widget.setLayout(layout)

        self.load_student_info()

    def setup_menu(self):
        """
        Создает верхнее меню приложения.
        """
        menu_bar = self.menuBar()

        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction(QIcon.fromTheme("application-exit"), "Выход", self)
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)

        # Меню "Справка"
        help_menu = menu_bar.addMenu("Справка")
        about_action = QAction(QIcon.fromTheme("help-about"), "О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        about_autor = QAction(QIcon.fromTheme("help-about"), "Об Авторе", self)
        about_autor.triggered.connect(self.show_autor)
        help_menu.addAction(about_autor)

    def show_autor(self):
        from App.Interfice.AutorInfoWindow import AutorWindow
        self.autorWindow = AutorWindow()
        self.autorWindow.show()

    def show_about(self):
        from App.Interfice.AboutWindow import AboutWindow
        self.about_window = AboutWindow()
        self.about_window.exec()


    def close_application(self):
        from App.Interfice.Login import LoginWindow
        self.loginWindow = LoginWindow()
        self.loginWindow.show()
        self.close()


    def load_student_info(self):
        student_response = requests.get(f"http://localhost:8000/api/students/{self.student_id}", headers={"Authorization": f"Bearer {self.token}"})
        if student_response.status_code == 200:
            student_data = student_response.json()
            self.student_info_label.setText(f"Имя Фавмилия: {student_data['first_name']} {student_data['last_name']}\n"
                                            f"Дата рождения: {student_data['birth_date']}\n"
                                            f"Контактная информация: {student_data['contact_info']}\n"
                                            f"курс: {student_data['course']}\n"
                                            f"Группа: {student_data['grup']}\n"
                                            f"Пол: {student_data['gender']}")


            violations_response = requests.get(f"http://localhost:8000/api/violations/", headers={"Authorization": f"Bearer {self.token}"})
            if violations_response.status_code == 200:
                violations_data = violations_response.json()
                self.len_violations_table = 0

                for row, violation in enumerate(violations_data):
                    if int(violation["student_id"]) == self.student_id:
                        self.len_violations_table+=1


                self.violations_table.setRowCount(self.len_violations_table)

                for row, violation in enumerate(violations_data):
                    if int(violation["student_id"]) == self.student_id:
                        self.violations_table.setItem(row, 1, QTableWidgetItem(violation['description']))
                        self.violations_table.setItem(row, 2, QTableWidgetItem(violation['date']))