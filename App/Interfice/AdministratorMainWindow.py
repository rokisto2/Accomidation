from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import ( QPushButton)



class RoomButton(QPushButton):
    def __init__(self, room, token, parent=None):
        super().__init__(parent)
        self.room = room
        self.token = token
        self.setText(f"Комната {room['room_number']}")
        self.setFixedSize(100, 100)
        self.update_color()

    def update_color(self):
        if self.room['bed_count'] == self.room['occupied_beds']:
            # Полностью занятая комната
            self.setStyleSheet("""
                QPushButton {
                    background-color: #B0BEC5;  /* Светло-серый */
                    color: white;
                    font-weight: bold;
                    border: 1px solid #90A4AE;  /* Темнее фон для контраста */
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #CFD8DC;  /* Более светлый при наведении */
                }
            """)
        elif self.room['occupied_beds'] > 0:
            # Частично занятая комната
            self.setStyleSheet("""
                QPushButton {
                    background-color: #FFD54F;  /* Светло-оранжевый */
                    color: black;
                    font-weight: bold;
                    border: 1px solid #FFB300;  /* Темнее для контраста */
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #FFE082;  /* Более светлый при наведении */
                }
            """)
        else:
            # Свободная комната
            self.setStyleSheet("""
                QPushButton {
                    background-color: #C5E1A5;  /* Светло-зеленый */
                    color: black;
                    font-weight: bold;
                    border: 1px solid #9CCC65;  /* Темнее для контраста */
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #E6EE9C;  /* Более светлый при наведении */
                }
            """)


from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QTabWidget, QWidget, QComboBox, QLabel,
    QGridLayout, QScrollArea, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QLineEdit,
    QDateEdit, QDialogButtonBox, QMenuBar,
)
from PySide6.QtCore import Qt
import requests


class AdministratorMainWindow(QMainWindow):
    def __init__(self, token, dormitory_id):
        super().__init__()
        self.token = token
        self.dormitory_id = dormitory_id

        self.setWindowTitle("Система управления общежитиями")
        self.setGeometry(100, 100, 1200, 800)

        # Добавляем меню с кнопкой выхода
        self.setup_menu()

        # Создаем вкладки
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.rooms_tab = QWidget()
        self.tabs.addTab(self.rooms_tab, "Комнаты")

        # Устанавливаем содержимое вкладки комнат
        self.setup_rooms_tab()

    def setup_menu(self):
        """Добавляем меню с кнопкой выхода."""
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")

        # Добавляем действие "Выход"
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
        """
        Отображает информацию о программе.
        """
        QMessageBox.information(
            self,
            "Об авторе",
            "Author: Oleg Gaponenko\n"
            "Group Number: 10701323\n"
            "Email: gaponenkooleg@gmail.com\n"
        )

    def show_about(self):
        """
        Отображает информацию о программе.
        """
        QMessageBox.information(
            self,
            "О программе",
            "Система управления общежитиями\nВерсия 1.0\n"
            "Функционал:\n"
            "- Управление общежитиями: добавление, редактирование и удаление общежитий\n"
            "- Управление студентами: добавление, редактирование и удаление информации о студентах\n"
            "- Управление администраторами: добавление, редактирование и удаление администраторов общежитий\n"
            "- Управление работниками деканата: добавление, редактирование и удаление сотрудников деканата\n"
            "- Управление нарушениями: добавление, редактирование и удаление записей о нарушениях\n"
            "- Заселение и выселение студентов: управление процессом заселения и выселения студентов\n"
            "- Просмотр и редактирование информации о комнатах: управление данными о комнатах в общежитиях\n"
            "- Просмотр и редактирование информации о этажах: управление данными о этажах в общежитиях\n"
            "- Управление учетными записями пользователей: создание и управление учетными записями\n"
            "- Генерация отчетов и статистики: создание отчетов и статистических данных по различным параметрам"
        )

    def close_application(self):
        from App.Interfice.Login import LoginWindow
        self.loginWindow = LoginWindow()
        self.loginWindow.show()
        self.close()

    def setup_rooms_tab(self):
        layout = QVBoxLayout(self.rooms_tab)

        # Этажи
        self.floor_combo_box = QComboBox()
        self.floor_combo_box.currentIndexChanged.connect(self.load_rooms)
        layout.addWidget(QLabel("Выберите этаж:"))
        layout.addWidget(self.floor_combo_box)

        # Контейнер для кнопок комнат
        self.rooms_container = QWidget()
        self.rooms_layout = QGridLayout(self.rooms_container)
        self.rooms_layout.setSpacing(10)

        # Скроллинг
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.rooms_container)
        layout.addWidget(scroll_area)

        # Загрузка данных этажей
        self.load_floors()

    def load_floors(self):
        response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{self.dormitory_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            floors = response.json()
            self.floor_combo_box.clear()
            for floor in floors:
                self.floor_combo_box.addItem(f"Этаж {floor['floor_number']}", floor['id'])
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить этажи")

    def load_rooms(self):
        floor_id = self.floor_combo_box.currentData()
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()

            # Очистка предыдущего списка
            for i in reversed(range(self.rooms_layout.count())):
                widget = self.rooms_layout.takeAt(i).widget()
                if widget:
                    widget.deleteLater()

            # Добавление кнопок в сетку
            for index, room in enumerate(rooms):
                row, col = divmod(index, 8)
                room_button = RoomButton(room, self.token, parent=self.rooms_container)
                room_button.clicked.connect(lambda _, r=room: self.open_room_tab(r))
                self.rooms_layout.addWidget(room_button, row, col)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить комнаты")

    def open_room_tab(self, room):
        # Проверка, есть ли уже вкладка для комнаты
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == f"Комната {room['room_number']}":
                self.tabs.setCurrentIndex(i)
                return

        # Создаем новую вкладку
        room_tab = QWidget()
        layout = QVBoxLayout(room_tab)

        # Информация о комнате
        room_info = QLabel(f"Комната {room['room_number']}\n"
                           f"Мест: {room['bed_count']}\n"
                           f"Занято: {room['occupied_beds']}")
        layout.addWidget(room_info)

        # Таблица студентов
        students_table = QTableWidget()
        students_table.setColumnCount(5)
        students_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Группа", "Посмотреть акты", "Выписать акт"])
        layout.addWidget(students_table)

        # Загрузка данных студентов
        response = requests.get(f"http://localhost:8000/api/accommodations/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            accommodations = response.json()
            students = [
                requests.get(f"http://localhost:8000/api/students/{accommodation['student_id']}",
                             headers={"Authorization": f"Bearer {self.token}"}).json()
                for accommodation in accommodations if accommodation['room_id'] == room['id']
            ]
            students_table.setRowCount(len(students))
            for i, student in enumerate(students):
                students_table.setItem(i, 0, QTableWidgetItem(student['first_name']))
                students_table.setItem(i, 1, QTableWidgetItem(student['last_name']))
                students_table.setItem(i, 2, QTableWidgetItem(str(student['grup'])))

                # Кнопка "Посмотреть акты"
                view_button = QPushButton("Посмотреть акты")
                view_button.clicked.connect(lambda _, s=student: self.open_student_details(s))
                students_table.setCellWidget(i, 3, view_button)

                # Кнопка "Выписать акт"
                act_button = QPushButton("Выписать акт")
                act_button.clicked.connect(lambda _, s=student: self.add_act_dialog(s))
                students_table.setCellWidget(i, 4, act_button)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить студентов комнаты")

        # Добавляем вкладку
        self.tabs.addTab(room_tab, f"Комната {room['room_number']}")
        self.tabs.setCurrentWidget(room_tab)

    def open_student_details(self, student):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Акты студента {student['first_name']} {student['last_name']}")
        layout = QVBoxLayout(dialog)

        # Таблица актов
        acts_table = QTableWidget()
        acts_table.setColumnCount(2)
        acts_table.setHorizontalHeaderLabels(["Описание", "Дата"])
        layout.addWidget(acts_table)

        # Загрузка актов
        response = requests.get(f"http://localhost:8000/api/violations/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            violations = response.json()
            student_acts = [act for act in violations if act['student_id'] == student['id']]
            acts_table.setRowCount(len(student_acts))
            for i, act in enumerate(student_acts):
                acts_table.setItem(i, 0, QTableWidgetItem(act['description']))
                acts_table.setItem(i, 1, QTableWidgetItem(act['violation_date']))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить акты студента")

        dialog.setLayout(layout)
        dialog.exec()

    def add_act_dialog(self, student):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Выписать акт для {student['first_name']} {student['last_name']}")
        layout = QFormLayout(dialog)

        description_input = QLineEdit()
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        layout.addRow("Описание:", description_input)
        layout.addRow("Дата:", date_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(
            lambda: self.submit_act(student['id'], description_input.text(), date_input.date().toString("yyyy-MM-dd"),
                                    dialog)
        )
        buttons.rejected.connect(dialog.close)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec()

    def submit_act(self, student_id, description, date, dialog):
        data = {"student_id": student_id, "description": description, "date": date}
        response = requests.post(f"http://localhost:8000/api/violations/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Успех", "Акт выписан успешно")
            dialog.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось выписать акт")
