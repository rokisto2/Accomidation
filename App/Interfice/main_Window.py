from PySide6.QtWidgets import QMainWindow, QLabel, QComboBox, QVBoxLayout, QWidget, QMessageBox, QGridLayout
from PySide6.QtGui import QColor, QPainter, Qt
import requests

class RoomWidget(QWidget):
    def __init__(self, room_number, status, parent=None):
        super().__init__(parent)
        self.room_number = room_number
        self.status = status
        self.setFixedSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.status == "free":
            painter.setBrush(QColor("green"))
        elif self.status == "partially_occupied":
            painter.setBrush(QColor("blue"))
        else:
            painter.setBrush(QColor("red"))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.drawText(self.rect(), Qt.AlignCenter, f"Room {self.room_number}")

class MainWindow(QMainWindow):
    def __init__(self, role, token, dormitory_id=None):
        super().__init__()

        self.role = role
        self.token = token
        self.dormitory_id = dormitory_id
        self.all_rooms = []  # Атрибут для хранения всех комнат

        self.setWindowTitle("Main Window")

        # Create central widget and set it as the central widget of the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout and add widgets to it
        layout = QVBoxLayout()

        if self.role == "deanery_staff":
            self.dormitory_label = QLabel("Select Dormitory:")
            self.dormitory_combobox = QComboBox()
            layout.addWidget(self.dormitory_label)
            layout.addWidget(self.dormitory_combobox)
            self.load_dormitories()
            self.dormitory_combobox.currentIndexChanged.connect(self.load_floors)
        else:
            self.dormitory_label = QLabel(f"Dormitory: {self.get_dormitory_name(self.dormitory_id)}")
            layout.addWidget(self.dormitory_label)

        self.floor_label = QLabel("Select Floor:")
        self.floor_combobox = QComboBox()
        layout.addWidget(self.floor_label)
        layout.addWidget(self.floor_combobox)
        self.floor_combobox.currentIndexChanged.connect(self.filter_rooms_by_floor)

        self.rooms_layout = QGridLayout()
        layout.addLayout(self.rooms_layout)

        # Set the layout to the central widget
        central_widget.setLayout(layout)

        if self.role != "deanery_staff":
            self.load_floors()

        self.load_all_rooms()  # Загрузка всех комнат при инициализации

    def load_all_rooms(self):
        response = requests.get("http://localhost:8000/api/rooms/", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            self.all_rooms = response.json()
        else:
            QMessageBox.warning(self, "Error", "Failed to load rooms")

    def filter_rooms_by_floor(self):
        floor_id = self.floor_combobox.currentData()
        filtered_rooms = [room for room in self.all_rooms if room["floor_id"] == floor_id]
        self.display_rooms(filtered_rooms)

    def display_rooms(self, rooms):
        self.rooms_layout.setParent(None)
        self.rooms_layout = QGridLayout()
        row, col = 0, 0
        for room in rooms:
            if room["occupied_beds"] == 0:
                status = "free"
            elif room["occupied_beds"] < room["bed_count"]:
                status = "partially_occupied"
            else:
                status = "occupied"
            room_widget = RoomWidget(room["room_number"], status)
            self.rooms_layout.addWidget(room_widget, row, col)
            col += 1
            if col == 5:  # Change this value to adjust the number of columns
                col = 0
                row += 1
        self.centralWidget().layout().addLayout(self.rooms_layout)