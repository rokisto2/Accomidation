import requests
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QFormLayout, \
    QComboBox, QLineEdit, QMessageBox, QDialogButtonBox, QDateEdit, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt

class RoomWidget(QPushButton):
    def __init__(self, room, token, parent=None):
        super().__init__(parent)
        self.room = room
        self.token = token
        self.setText(f"Room {room['room_number']}")
        self.setFixedSize(100, 100)
        self.update_color()

    def update_color(self):
        if self.room['bed_count'] == self.room['occupied_beds']:
            self.setStyleSheet("background-color: red")
        elif self.room['occupied_beds'] > 0:
            self.setStyleSheet("background-color: yellow")
        else:
            self.setStyleSheet("background-color: green")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.room['occupied_beds'] > 0:
            self.show_room_details()

    def show_room_details(self):
        response = requests.get(f"http://localhost:8000/api/accommodations/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            accommodations = response.json()
            students = []
            for accommodation in accommodations:
                if accommodation['room_id'] == self.room['id']:
                    student_response = requests.get(f"http://localhost:8000/api/students/{accommodation['student_id']}",
                                                    headers={"Authorization": f"Bearer {self.token}"})
                    if student_response.status_code == 200:
                        students.append(student_response.json())

            dialog = QDialog(self)
            dialog.setWindowTitle(f"Room {self.room['room_number']} Details")
            dialog.setStyleSheet(self.parent().styleSheet())  # Apply the main window's stylesheet
            layout = QVBoxLayout(dialog)

            for student in students:
                student_button = QPushButton(f"{student['first_name']} {student['last_name']} (Group {student['grup']})", dialog)
                student_button.clicked.connect(lambda _, s=student: self.show_student_details(s))
                layout.addWidget(student_button)
                add_act_button = QPushButton("Add Act")
                add_act_button.clicked.connect(lambda: self.add_act(student['id'], dialog))
                layout.addWidget(add_act_button)

            dialog.setLayout(layout)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "Failed to load room details")

    def show_student_details(self, student):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Student {student['first_name']} {student['last_name']} Details")
        dialog.setStyleSheet(self.parent().styleSheet())  # Apply the main window's stylesheet
        layout = QVBoxLayout(dialog)

        # Add student details
        details = QLabel(f"Name: {student['first_name']} {student['last_name']}\n"
                         f"Birth Date: {student['birth_date']}\n"
                         f"Contact Info: {student['contact_info']}\n"
                         f"Course: {student['course']}\n"
                         f"Group: {student['grup']}\n"
                         f"Is Non Local: {student['is_non_local']}\n"
                         f"Gender: {student['gender']}", dialog)
        layout.addWidget(details)

        # Add table with acts
        acts_table = QTableWidget(dialog)
        acts_table.setColumnCount(2)
        acts_table.setHorizontalHeaderLabels(["Description", "Date"])

        acts_response = requests.get(f"http://localhost:8000/api/violations/",
                                     headers={"Authorization": f"Bearer {self.token}"})
        if acts_response.status_code == 200:
            acts = acts_response.json()
            student_acts = [act for act in acts if act['student_id'] == student['id']]
            acts_table.setRowCount(len(student_acts))
            for row, act in enumerate(student_acts):
                acts_table.setItem(row, 0, QTableWidgetItem(act['description']))
                acts_table.setItem(row, 1, QTableWidgetItem(act['violation_date']))
                # Add actions if needed

        layout.addWidget(acts_table)
        dialog.setLayout(layout)
        dialog.exec()

    def add_act(self, student_id, parent_dialog):
        act_dialog = QDialog(parent_dialog)
        act_dialog.setWindowTitle("Add Act")
        act_dialog.setStyleSheet(self.parent().styleSheet())  # Apply the main window's stylesheet
        layout = QFormLayout(act_dialog)

        description_input = QLineEdit(act_dialog)
        date_input = QDateEdit(act_dialog)
        date_input.setCalendarPopup(True)
        date_input.setDisplayFormat("yyyy-MM-dd")

        layout.addRow("Description:", description_input)
        layout.addRow("Date:", date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, act_dialog)
        buttons.accepted.connect(
            lambda: self.submit_act(student_id, description_input.text(), date_input.date().toString("yyyy-MM-dd"),
                                    act_dialog))
        buttons.rejected.connect(act_dialog.close)
        layout.addWidget(buttons)

        act_dialog.setLayout(layout)
        act_dialog.exec()

    def submit_act(self, student_id, description, date, act_dialog):
        data = {
            "student_id": int(student_id),
            "description": description,
            "date": date
        }
        response = requests.post("http://localhost:8000/api/violations/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Add Act", "Act added successfully")
            act_dialog.close()
        else:
            QMessageBox.warning(self, "Add Act", "Failed to add act")

class AdministratorMainWindow(QMainWindow):
    def __init__(self, token, dormitory_id):
        super().__init__()
        self.token = token
        self.dormitory_id = dormitory_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Administrator Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.floor_combo_box = QComboBox()
        self.floor_combo_box.currentIndexChanged.connect(self.load_rooms)
        self.layout.addWidget(self.floor_combo_box)

        self.rooms_layout = QVBoxLayout()
        self.layout.addLayout(self.rooms_layout)

        self.load_floors()

        container = QDialog()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_floors(self):
        response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{self.dormitory_id}", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            floors = response.json()
            self.floor_combo_box.clear()
            for floor in floors:
                self.floor_combo_box.addItem(f"Floor {floor['floor_number']}", floor['id'])
        else:
            QMessageBox.warning(self, "Error", "Failed to load floors")

    def load_rooms(self):
        floor_id = self.floor_combo_box.currentData()
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()
            self.clear_layout(self.rooms_layout)
            for room in rooms:
                room_widget = RoomWidget(room, self.token)
                self.rooms_layout.addWidget(room_widget)
        else:
            QMessageBox.warning(self, "Error", "Failed to load rooms")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()