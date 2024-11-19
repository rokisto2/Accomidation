import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QWidget, QPushButton, QLineEdit, \
    QLabel, QFormLayout, QDialog, QDialogButtonBox, QComboBox, QTableWidget, QTableWidgetItem, QDateEdit, QInputDialog, \
    QCheckBox
import sys

from App.Interfice.Login import LoginWindow


class DeaneryStaffMainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Deanery Staff Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.add_dormitory_button = QPushButton("Add Dormitory")
        self.add_dormitory_button.clicked.connect(self.show_add_dormitory_dialog)
        self.layout.addWidget(self.add_dormitory_button)

        self.manage_dormitories_button = QPushButton("Manage Dormitories")
        self.manage_dormitories_button.clicked.connect(self.show_manage_dormitories_dialog)
        self.layout.addWidget(self.manage_dormitories_button)

        self.add_student_button = QPushButton("Assign Student", self)
        self.add_student_button.clicked.connect(self.show_add_student_dialog)
        self.layout.addWidget(self.add_student_button)

        self.add_deanery_staff_button = QPushButton("Assign Deanery Staff", self)
        self.add_deanery_staff_button.clicked.connect(self.show_add_deanery_staff_dialog)
        self.layout.addWidget(self.add_deanery_staff_button)

        self.assign_administrators_button = QPushButton("Assign Administrators")
        self.assign_administrators_button.clicked.connect(self.show_assign_administrators_dialog)
        self.layout.addWidget(self.assign_administrators_button)

        self.add_violations_button = QPushButton("Add Violations")
        self.add_violations_button.clicked.connect(self.show_add_violations_dialog)
        self.layout.addWidget(self.add_violations_button)

        self.distribute_students_button = QPushButton("Distribute Students")
        self.distribute_students_button.clicked.connect(self.distribute_students)
        self.layout.addWidget(self.distribute_students_button)

        self.evict_students_button = QPushButton("Evict Students")
        self.evict_students_button.clicked.connect(self.show_evict_students_dialog)
        self.layout.addWidget(self.evict_students_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.show_login_window)
        self.layout.addWidget(self.exit_button)

    def show_login_window(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def show_add_dormitory_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Dormitory")
        layout = QFormLayout(dialog)

        name_input = QLineEdit(dialog)
        address_input = QLineEdit(dialog)
        description_input = QLineEdit(dialog)

        layout.addRow("Name:", name_input)
        layout.addRow("Address:", address_input)
        layout.addRow("Description:", description_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_dormitory(name_input.text(), address_input.text(), description_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def add_dormitory(self, name, address, description, dialog):
        data = {
            "name": name,
            "address": address,
            "description": description
        }
        response = requests.post("http://localhost:8000/api/dormitories/", json=data, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Add Dormitory", "Dormitory added successfully")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Add Dormitory", "Failed to add dormitory")

    def show_manage_dormitories_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Dormitories")
        layout = QVBoxLayout(dialog)

        dormitory_combo = QComboBox(dialog)
        self.populate_dormitory_combo(dormitory_combo)
        layout.addWidget(dormitory_combo)

        floor_combo = QComboBox(dialog)
        dormitory_combo.currentIndexChanged.connect(
            lambda: self.populate_floor_combo(dormitory_combo.currentData(), floor_combo))
        layout.addWidget(floor_combo)

        add_floor_button = QPushButton("Add Floor", dialog)
        add_floor_button.clicked.connect(lambda: self.add_floor(dormitory_combo.currentData(), floor_combo, dialog))
        layout.addWidget(add_floor_button)

        room_type_combo = QComboBox(dialog)
        room_type_combo.addItems(["male", "female", "family"])
        layout.addWidget(QLabel("Room Type:", dialog))
        layout.addWidget(room_type_combo)

        bed_count_input = QLineEdit(dialog)
        layout.addWidget(QLabel("Bed Count:", dialog))
        layout.addWidget(bed_count_input)

        add_room_button = QPushButton("Add Room", dialog)
        add_room_button.clicked.connect(
            lambda: self.add_room(floor_combo.currentData(), room_type_combo.currentText(), bed_count_input.text(),
                                  dialog))
        layout.addWidget(add_room_button)

        remove_room_button = QPushButton("Remove Room", dialog)
        remove_room_button.clicked.connect(lambda: self.remove_room(floor_combo.currentData(), dialog))
        layout.addWidget(remove_room_button)

        dialog.exec()

    def show_add_student_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Student")
        layout = QFormLayout(dialog)

        first_name_input = QLineEdit(dialog)
        last_name_input = QLineEdit(dialog)
        birth_date_input = QDateEdit(dialog)
        birth_date_input.setCalendarPopup(True)
        birth_date_input.setDisplayFormat("yyyy-MM-dd")
        contact_info_input = QLineEdit(dialog)
        course_input = QLineEdit(dialog)
        grup_input = QLineEdit(dialog)
        is_non_local_input = QCheckBox(dialog)
        password_input = QLineEdit(dialog)
        gender_input = QComboBox(dialog)
        gender_input.addItems(["male", "female"])

        layout.addRow("First Name:", first_name_input)
        layout.addRow("Last Name:", last_name_input)
        layout.addRow("Birth Date:", birth_date_input)
        layout.addRow("Contact Info:", contact_info_input)
        layout.addRow("Course:", course_input)
        layout.addRow("Group:", grup_input)
        layout.addRow("Is Non Local:", is_non_local_input)
        layout.addRow("Password:", password_input)
        layout.addRow("Gender:", gender_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_student(first_name_input.text(), last_name_input.text(),
                                                          birth_date_input.date().toString("yyyy-MM-dd"),
                                                          contact_info_input.text(), course_input.text(),
                                                          grup_input.text(), is_non_local_input.isChecked(),
                                                          password_input.text(), gender_input.currentText(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def show_add_deanery_staff_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Deanery Staff")
        layout = QFormLayout(dialog)

        first_name_input = QLineEdit(dialog)
        last_name_input = QLineEdit(dialog)
        contact_info_input = QLineEdit(dialog)
        password_input = QLineEdit(dialog)

        layout.addRow("First Name:", first_name_input)
        layout.addRow("Last Name:", last_name_input)
        layout.addRow("Contact Info:", contact_info_input)
        layout.addRow("Password:", password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(
            lambda: self.add_deanery_staff(first_name_input.text(), last_name_input.text(), contact_info_input.text(),
                                           password_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def add_deanery_staff(self, first_name, last_name, contact_info, password, dialog):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "contact_info": contact_info,
            "password": password
        }
        response = requests.post("http://localhost:8000/api/deanery_staff/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Add Deanery Staff", "Deanery staff added successfully")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Add Deanery Staff", "Failed to add deanery staff")

    def add_student(self, first_name, last_name, birth_date, contact_info, course, grup, is_non_local, password, gender,
                    dialog):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "contact_info": contact_info,
            "course": int(course),
            "grup": int(grup),
            "is_non_local": is_non_local,
            "password": password,
            "gender": gender
        }
        response = requests.post("http://localhost:8000/api/students/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Add Student", "Student added successfully")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Add Student", "Failed to add student")


    def populate_dormitory_combo(self, combo):
        response = requests.get("http://localhost:8000/api/dormitories/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            dormitories = response.json()
            combo.clear()
            for dormitory in dormitories:
                combo.addItem(dormitory['name'], dormitory['id'])
        else:
            QMessageBox.warning(self, "Dormitories", "Failed to retrieve dormitories")

    def populate_room_combo(self, floor_id, combo):
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()
            combo.clear()
            for room in rooms:
                combo.addItem(f"Room {room['room_number']}", room['id'])
        else:
            QMessageBox.warning(self, "Rooms", "Failed to retrieve rooms")

    def populate_floor_combo(self, dormitory_id, combo):
        if dormitory_id is None:
            pass
        else:
            response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{dormitory_id}",
                                    headers={"Authorization": f"Bearer {self.token}"})

            combo.clear()

            if response.status_code == 200:
                floors = response.json()
                for floor in floors:
                    combo.addItem(f"Floor {floor['floor_number']}", floor['id'])
            elif response.status_code == 404:
                QMessageBox.warning(self, "Load Floors", "No floors found")
            else:
                QMessageBox.warning(self, "Load Floors", "Failed to retrieve floors")

    def add_floor(self, dormitory_id, floor_combo, dialog):


        response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{dormitory_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            floors = response.json()
            next_floor_number = max(floor['floor_number'] for floor in floors) + 1 if floors else 1
        elif response.status_code == 404:
            next_floor_number = 1
        else:
            QMessageBox.warning(dialog, "Add Floor", "Failed to retrieve floors")
            return

        data = {
            "dormitory_id": dormitory_id,
            "floor_number": next_floor_number
        }
        response = requests.post("http://localhost:8000/api/floors/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            self.populate_floor_combo(dormitory_id, floor_combo)
            QMessageBox.information(dialog, "Add Floor", f"Floor {next_floor_number} added successfully")
        else:
            QMessageBox.warning(dialog, "Add Floor", "Failed to add floor")


    def add_room(self, floor_id, room_type, bed_count, dialog):
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()
            next_room_number = max(room['room_number'] for room in rooms) + 1 if rooms else 1
            data = {
                "floor_id": floor_id,
                "room_type": room_type,
                "room_number": next_room_number,
                "bed_count": int(bed_count)  # Ensure bed_count is an integer
            }
            response = requests.post("http://localhost:8000/api/rooms/", json=data,
                                     headers={"Authorization": f"Bearer {self.token}"})
            if response.status_code == 200:
                QMessageBox.information(dialog, "Add Room", f"Room {next_room_number} added successfully")
            else:
                QMessageBox.warning(dialog, "Add Room", "Failed to add room")
        else:
            QMessageBox.warning(dialog, "Add Room", "Failed to retrieve rooms")

    def remove_room(self, floor_id, dialog):
        room_combo = QComboBox(dialog)
        self.populate_room_combo(floor_id, room_combo)

        def confirm_removal():
            room_id = room_combo.currentData()
            response = requests.get(f"http://localhost:8000/api/accommodations/?room_id={room_id}",
                                    headers={"Authorization": f"Bearer {self.token}"})
            if response.status_code == 200:
                accommodations = response.json()
                if accommodations:
                    QMessageBox.warning(dialog, "Remove Room",
                                        "Cannot remove room. Students are currently accommodated in this room.")
                else:
                    response = requests.delete(f"http://localhost:8000/api/rooms/{room_id}",
                                               headers={"Authorization": f"Bearer {self.token}"})
                    if response.status_code == 200:
                        QMessageBox.information(dialog, "Remove Room", "Room removed successfully")
                    else:
                        QMessageBox.warning(dialog, "Remove Room", "Failed to remove room")
            else:
                QMessageBox.warning(dialog, "Remove Room", "Failed to check accommodations")

        dialog = QDialog(self)
        dialog.setWindowTitle("Remove Room")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Select Room:", dialog))
        layout.addWidget(room_combo)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(confirm_removal)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec()



    def remove_floor(self, dormitory_id, floor_number, dialog):
        response = requests.delete(f"http://localhost:8000/api/floors/{floor_number}", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Manage Dormitories", "Floor removed successfully")
        else:
            QMessageBox.warning(self, "Manage Dormitories", "Failed to remove floor")

    def show_assign_administrators_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Assign Administrators")
        layout = QFormLayout(dialog)

        first_name_input = QLineEdit(dialog)
        last_name_input = QLineEdit(dialog)
        contact_info_input = QLineEdit(dialog)
        dormitory_id_input = QLineEdit(dialog)
        password_input = QLineEdit(dialog)

        layout.addRow("First Name:", first_name_input)
        layout.addRow("Last Name:", last_name_input)
        layout.addRow("Contact Info:", contact_info_input)
        layout.addRow("Dormitory ID:", dormitory_id_input)
        layout.addRow("Password:", password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.assign_administrators(first_name_input.text(), last_name_input.text(), contact_info_input.text(), dormitory_id_input.text(), password_input.text(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def assign_administrators(self, first_name, last_name, contact_info, dormitory_id, password, dialog):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "contact_info": contact_info,
            "dormitory_id": int(dormitory_id),
            "password": password
        }
        response = requests.post("http://localhost:8000/api/administration/", json=data, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Assign Administrators", "Administrator assigned successfully")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Assign Administrators", "Failed to assign administrator")

    def show_add_violations_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Violations")
        layout = QFormLayout(dialog)

        student_combo = QComboBox(dialog)
        self.populate_student_combo(student_combo)

        description_input = QLineEdit(dialog)
        date_input = QDateEdit(dialog)
        date_input.setCalendarPopup(True)
        date_input.setDisplayFormat("yyyy-MM-dd")

        layout.addRow("Student:", student_combo)
        layout.addRow("Description:", description_input)
        layout.addRow("Date:", date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_violations(student_combo.currentData(), description_input.text(),
                                                             date_input.date().toString("yyyy-MM-dd"), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def populate_student_combo(self, combo):
        response = requests.get("http://localhost:8000/api/students/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            students = response.json()
            for student in students:
                accommodation_response = requests.get(f"http://localhost:8000/api/accommodations/{student['id']}",
                                                      headers={"Authorization": f"Bearer {self.token}"})
                if accommodation_response.status_code == 200:
                    combo.addItem(f"{student['first_name']} {student['last_name']} (Group {student['grup']})",
                                  student['id'])
        else:
            QMessageBox.warning(self, "Add Violations", "Failed to retrieve students")

    def add_violations(self, student_id, description, date, dialog):
        data = {
            "student_id": int(student_id),
            "description": description,
            "date": date
        }
        response = requests.post("http://localhost:8000/api/violations/", json=data, headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Add Violations", "Violation added successfully")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Add Violations", "Failed to add violation")

    def distribute_students(self):
        response = requests.post("http://localhost:8000/api/accommodations/distribute", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Distribute Students", "Students distributed successfully")
            self.show_accommodations_table()
        else:
            QMessageBox.warning(self, "Distribute Students", "Failed to distribute students")

    def show_accommodations_table(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Accommodated Students")
        layout = QVBoxLayout(dialog)

        table = QTableWidget(dialog)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Student", "Group", "Date From", "Dormitory"])

        response = requests.get("http://localhost:8000/api/accommodations/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            accommodations = response.json()
            table.setRowCount(len(accommodations))
            for row, accommodation in enumerate(accommodations):
                student_response = requests.get(f"http://localhost:8000/api/students/{accommodation['student_id']}",
                                                headers={"Authorization": f"Bearer {self.token}"})
                room_response = requests.get(f"http://localhost:8000/api/rooms/{accommodation['room_id']}",
                                             headers={"Authorization": f"Bearer {self.token}"})
                if student_response.status_code == 200 and room_response.status_code == 200:
                    student = student_response.json()
                    room = room_response.json()
                    floor_response = requests.get(f"http://localhost:8000/api/floors/{room['floor_id']}",
                                                  headers={"Authorization": f"Bearer {self.token}"})
                    if floor_response.status_code == 200:
                        floor = floor_response.json()
                        dormitory_response = requests.get(
                            f"http://localhost:8000/api/dormitories/{floor['dormitory_id']}",
                            headers={"Authorization": f"Bearer {self.token}"})
                        if dormitory_response.status_code == 200:
                            dormitory = dormitory_response.json()
                            table.setItem(row, 0, QTableWidgetItem(student['first_name'] + " " + student['last_name']))
                            table.setItem(row, 1, QTableWidgetItem(str(student['grup'])))
                            table.setItem(row, 2, QTableWidgetItem(accommodation['date_from']))
                            table.setItem(row, 3, QTableWidgetItem(dormitory['name']))
        else:
            QMessageBox.warning(self, "Accommodated Students", "Failed to retrieve accommodations")

        layout.addWidget(table)
        dialog.exec()

    def show_evict_students_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Evict Students")
        layout = QFormLayout(dialog)

        student_combo = QComboBox(dialog)
        self.populate_student_combo(student_combo)

        layout.addRow("Student:", student_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.evict_students(student_combo.currentData(), dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def evict_students(self, student_id, dialog):
        response = requests.delete(f"http://localhost:8000/api/accommodations/evict/{student_id}", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Evict Students", "Student evicted successfully")
            dialog.accept()
        else:
            QMessageBox.warning(self, "Evict Students", "Failed to evict student")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    token = "your_jwt_token_here"  # Replace with actual token
    window = DeaneryStaffMainWindow(token)
    window.show()
    sys.exit(app.exec())