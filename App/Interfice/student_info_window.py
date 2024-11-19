from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QWidget
import requests

class StudentInfoWindow(QMainWindow):
    def __init__(self, token, student_id):
        super().__init__()
        self.token = token
        self.student_id = student_id

        self.setWindowTitle("Student Information")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.student_info_label = QLabel("Student Information")
        layout.addWidget(self.student_info_label)

        self.room_info_label = QLabel("Room Information")
        layout.addWidget(self.room_info_label)

        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(2)
        self.violations_table.setHorizontalHeaderLabels(["Description", "Date"])
        layout.addWidget(self.violations_table)

        central_widget.setLayout(layout)

        self.load_student_info()

    def load_student_info(self):
        student_response = requests.get(f"http://localhost:8000/api/students/{self.student_id}", headers={"Authorization": f"Bearer {self.token}"})
        if student_response.status_code == 200:
            student_data = student_response.json()
            self.student_info_label.setText(f"Name: {student_data['first_name']} {student_data['last_name']}\n"
                                            f"Birth Date: {student_data['birth_date']}\n"
                                            f"Contact Info: {student_data['contact_info']}\n"
                                            f"Course: {student_data['course']}\n"
                                            f"Group: {student_data['grup']}\n"
                                            f"Gender: {student_data['gender']}")

            accommodation_response = requests.get(f"http://localhost:8000/api/accommodations/?student_id={self.student_id}", headers={"Authorization": f"Bearer {self.token}"})
            if accommodation_response.status_code == 200:
                accommodation_data = accommodation_response.json()
                if accommodation_data:
                    room_id = accommodation_data[0]['room_id']
                    room_response = requests.get(f"http://localhost:8000/api/rooms/{room_id}", headers={"Authorization": f"Bearer {self.token}"})
                    if room_response.status_code == 200:
                        room_data = room_response.json()
                        self.room_info_label.setText(f"Room Number: {room_data['room_number']}")

            violations_response = requests.get(f"http://localhost:8000/api/violations/?student_id={self.student_id}", headers={"Authorization": f"Bearer {self.token}"})
            if violations_response.status_code == 200:
                violations_data = violations_response.json()
                self.violations_table.setRowCount(len(violations_data))
                for row, violation in enumerate(violations_data):
                    self.violations_table.setItem(row, 1, QTableWidgetItem(violation['description']))
                    self.violations_table.setItem(row, 2, QTableWidgetItem(violation['date']))