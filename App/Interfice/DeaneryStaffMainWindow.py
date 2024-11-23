import requests

from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QLineEdit, QDateEdit, QCheckBox, QHBoxLayout, QMessageBox, QComboBox, QDialogButtonBox
)
import sys


class DeaneryStaffMainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Система управления общежитиями")
        self.setGeometry(100, 100, 1200, 800)

        # Восстановление панели инструментов и меню
        self.setup_menu()

        # Центральный виджет с вкладками
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)  # Включение возможности закрытия вкладок
        self.tabs.tabCloseRequested.connect(self.close_tab)  # Подключение сигнала к слоту
        self.setCentralWidget(self.tabs)

        # Создание вкладок
        self.dormitories_tab = QWidget()
        self.students_tab = QWidget()
        self.staff_tab = QWidget()
        self.violations_tab = QWidget()
        self.admins_tab = QWidget()

        self.tabs.addTab(self.dormitories_tab, "Общежития")
        self.tabs.addTab(self.students_tab, "Студенты")
        self.tabs.addTab(self.admins_tab, "Администраторы")

        self.tabs.addTab(self.staff_tab, "Работники деканата")
        self.tabs.addTab(self.violations_tab, "Нарушения")



        # Установка содержимого вкладок
        self.setup_dormitories_tab()
        self.setup_admins_tab()
        self.setup_students_tab()
        self.setup_staff_tab()
        self.setup_violations_tab()

        self.accommodate_tab = QWidget()
        self.setup_accommodate_tab()
        self.tabs.addTab(self.accommodate_tab, "Заселение")

        self.evict_tab = QWidget()
        self.setup_evict_tab()
        self.tabs.addTab(self.evict_tab, "Выселение")

    def setup_accommodate_tab(self):
        layout = QVBoxLayout(self.accommodate_tab)

        dormitory_combo = QComboBox()
        self.populate_dormitory_combo(dormitory_combo)
        layout.addWidget(QLabel("Выберите общежитие:"))
        layout.addWidget(dormitory_combo)

        self.floor_combo = QComboBox()
        dormitory_combo.currentIndexChanged.connect(
            lambda: self.load_floor_combo(dormitory_combo.currentData(), self.floor_combo))
        layout.addWidget(QLabel("Выберите этаж:"))
        layout.addWidget(self.floor_combo)

        self.room_combo = QComboBox()
        self.floor_combo.currentIndexChanged.connect(lambda: self.load_room_combo(self.floor_combo.currentData(), self.room_combo))
        layout.addWidget(QLabel("Выберите комнату:"))
        layout.addWidget(self.room_combo)

        self.unassigned_student_combo = QComboBox()
        self.populate_student_combos()
        layout.addWidget(QLabel("Выберите студента:"))
        layout.addWidget(self.unassigned_student_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(
            lambda: self.accommodate_student(self.unassigned_student_combo.currentData(), self.room_combo.currentData()))
        buttons.rejected.connect(lambda: self.tabs.setCurrentWidget(self.students_tab))
        layout.addWidget(buttons)

        self.accommodate_tab.setLayout(layout)


    def load_floor_combo(self, dormitory_id, combo):
        response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{dormitory_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            floors = response.json()
            combo.clear()
            for floor in floors:
                combo.addItem(f"Этаж {floor['floor_number']}", floor["id"])
            if floors:
                combo.setCurrentIndex(0)  # Select the first item
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить этажи")

    def load_room_combo(self, floor_id, combo):
        room_type_translation = {"male": "Мужская", "female": "Женская", "family": "Семейная"}
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()
            combo.clear()
            for room in rooms:
                if room['occupied_beds'] < room['bed_count']:  # Only show rooms with available beds
                    room_type_russian = room_type_translation.get(room['room_type'], room['room_type'])
                    combo.addItem(
                        f"Комната {room['room_number']} ({room_type_russian}, {room['bed_count']} мест, занято {room['occupied_beds']})",
                        room['id'])
            if rooms:
                combo.setCurrentIndex(0)  # Select the first item
        elif response.status_code == 422:
            pass
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить комнаты")

    def populate_room_combo(self, floor_id, combo):
        room_type_translation = {"male": "Мужская", "female": "Женская", "family": "Семейная"}
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()
            combo.clear()
            for room in rooms:
                room_type_russian = room_type_translation.get(room['room_type'], room['room_type'])
                combo.addItem(f"Комната {room['room_number']} ({room_type_russian}, {room['bed_count']} мест)",
                              room['id'])
            if rooms:
                combo.setCurrentIndex(0)  # Select the first item
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить комнаты")


    def setup_evict_tab(self):
        layout = QVBoxLayout(self.evict_tab)

        self.assigned_student_combo = QComboBox()
        self.populate_student_combos()

        layout.addWidget(QLabel("Выберите студента:"))
        layout.addWidget(self.assigned_student_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.evict_student(self.assigned_student_combo.currentData()))
        buttons.rejected.connect(lambda: self.tabs.setCurrentWidget(self.students_tab))
        layout.addWidget(buttons)

        self.evict_tab.setLayout(layout)

    def populate_student_combos(self):
        response_students = requests.get("http://localhost:8000/api/students/")
        response_accommodations = requests.get("http://localhost:8000/api/accommodations/")

        if response_students.status_code == 200 and response_accommodations.status_code == 200:
            students = response_students.json()
            accommodations = response_accommodations.json()
            assigned_student_ids = {accommodation['student_id'] for accommodation in accommodations}

            unassigned_students = [student for student in students if student['id'] not in assigned_student_ids]
            assigned_students = [student for student in students if student['id'] in assigned_student_ids]
            try:
                self.populate_combo(self.unassigned_student_combo, unassigned_students)
            except:
                pass
            try:
                self.populate_combo(self.assigned_student_combo, assigned_students)
            except:
                pass
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные студентов или заселений")

    def populate_combo(self, combo, students):
        combo.clear()
        for student in students:
            combo.addItem(f"{student['first_name']} {student['last_name']}", student['id'])

    def update_occupied_beds(self, room_id, increment):
        response = requests.get(f"http://localhost:8000/api/rooms/{room_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            room = response.json()
            new_occupied_beds = room['occupied_beds'] + 1 if increment else room['occupied_beds'] - 1
            data = {"occupied_beds": new_occupied_beds,
                    "room_type": room['room_type'],
                    "room_number": room['room_number'],
                    "floor_id": room['floor_id'],
                    "bed_count": room['bed_count']}
            update_response = requests.put(f"http://localhost:8000/api/rooms/{room_id}", json=data,
                                           headers={"Authorization": f"Bearer {self.token}"})
            if update_response.status_code != 200:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить количество занятых мест в комнате")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные комнаты")

    def accommodate_student(self, student_id, room_id):
        data = {"student_id": student_id, "room_id": room_id, "date_from": "2023-01-01"}
        response = requests.post("http://localhost:8000/api/accommodations/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            # Update the occupied beds count
            self.update_occupied_beds(room_id, increment=True)
            QMessageBox.information(self, "Успех", "Студент успешно заселен")
            self.populate_student_combos()
            self.load_room_combo(self.floor_combo.currentData(), self.room_combo)  # Refresh room list
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось заселить студента")

    def evict_student(self, student_id):
        response = requests.delete(f"http://localhost:8000/api/accommodations/evict/{student_id}",
                                   headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            # Get the room_id from the accommodation details
            accommodation = response.json()
            room_id = accommodation['room_id']
            # Update the occupied beds count
            self.update_occupied_beds(room_id, increment=False)
            QMessageBox.information(self, "Успех", "Студент успешно выселен")
            self.populate_student_combos()
            self.load_room_combo(self.floor_combo.currentData(), self.room_combo)     # Refresh room list
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось выселить студента")

    def close_tab(self, index):
        """
        Закрывает вкладку по индексу.
        """
        if index>4:
            self.tabs.removeTab(index)
        else:
            QMessageBox.warning(self, "Ошибка", "Эту вкладку нельзя закрыть")



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


    def close_application(self):
        from App.Interfice.Login import LoginWindow
        self.loginWindow = LoginWindow()
        self.loginWindow.show()
        self.close()

    def setup_toolbar(self):
        """
        Создает панель инструментов приложения.
        """
        toolbar = self.addToolBar("Основные действия")

        # Кнопка добавления общежития
        add_dorm_action = QAction(QIcon.fromTheme("list-add"), "Добавить общежитие", self)
        add_dorm_action.triggered.connect(self.add_dormitory_widget)
        toolbar.addAction(add_dorm_action)

        # Кнопка добавления студента
        add_student_action = QAction(QIcon.fromTheme("user-add"), "Добавить студента", self)
        add_student_action.triggered.connect(self.add_student_widget)
        toolbar.addAction(add_student_action)


        # Кнопка добавления нарушения
        violations_action = QAction(QIcon.fromTheme("dialog-warning"), "Добавить нарушение", self)
        violations_action.triggered.connect(self.add_violation_widget)
        toolbar.addAction(violations_action)


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

    def setup_admins_tab(self):
        layout = QVBoxLayout(self.admins_tab)

        # Таблица для отображения администраторов
        self.admins_table = QTableWidget()
        self.admins_table.setColumnCount(4)
        self.admins_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Контакты", "Общежитие"])
        layout.addWidget(self.admins_table)

        # Управляющая кнопка
        add_admin_button = QPushButton("Добавить администратора")
        add_admin_button.clicked.connect(self.add_admin_widget)
        layout.addWidget(add_admin_button)

        self.load_admins()

    def load_admins(self):
        response = requests.get("http://localhost:8000/api/administration/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            admins = response.json()
            self.admins_table.setRowCount(len(admins))
            for i, admin in enumerate(admins):
                dormitory_response = requests.get(f"http://localhost:8000/api/dormitories/{admin['dormitory_id']}",
                                                  headers={"Authorization": f"Bearer {self.token}"})
                dormitory_name = dormitory_response.json()[
                    'name'] if dormitory_response.status_code == 200 else "Неизвестно"
                self.admins_table.setItem(i, 0, QTableWidgetItem(admin['first_name']))
                self.admins_table.setItem(i, 1, QTableWidgetItem(admin['last_name']))
                self.admins_table.setItem(i, 2, QTableWidgetItem(admin['contact_info']))
                self.admins_table.setItem(i, 3, QTableWidgetItem(dormitory_name))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить администраторов")

    def add_admin_widget(self):
        fields = ["Имя", "Фамилия", "Контакты", "Общежитие", "Пароль"]
        self.add_form_widget("Добавить администратора", fields, self.add_admin)

    def add_admin(self, inputs):
        data = {
            "first_name": inputs["Имя"].text(),
            "last_name": inputs["Фамилия"].text(),
            "contact_info": inputs["Контакты"].text(),
            "dormitory_id": int(inputs["Общежитие"].currentData()),
            "password": inputs["Пароль"].text()
        }
        response = requests.post("http://localhost:8000/api/administration/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Успех", "Администратор успешно добавлен")
            self.load_admins()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить администратора")

    def setup_dormitories_tab(self):
        layout = QVBoxLayout(self.dormitories_tab)

        # Таблица для отображения списка общежитий
        self.dormitories_table = QTableWidget()
        self.dormitories_table.setColumnCount(3)
        self.dormitories_table.setHorizontalHeaderLabels(["Название", "Адрес", "Описание"])
        layout.addWidget(self.dormitories_table)

        # Управляющие кнопки
        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить общежитие")
        add_button.clicked.connect(self.add_dormitory_widget)
        button_layout.addWidget(add_button)

        manage_button = QPushButton("Управление этажами и комнатами")
        manage_button.clicked.connect(self.manage_dormitory_widget)
        button_layout.addWidget(manage_button)

        layout.addLayout(button_layout)
        self.load_dormitories()

    def manage_dormitory_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Выбор общежития
        dormitory_label = QLabel("Выберите общежитие:")
        dormitory_combo = QComboBox()
        self.populate_dormitory_combo(dormitory_combo)
        layout.addWidget(dormitory_label)
        layout.addWidget(dormitory_combo)

        # Выбор этажа
        floor_label = QLabel("Выберите этаж:")
        floor_combo = QComboBox()
        dormitory_combo.currentIndexChanged.connect(
            lambda: self.populate_floor_combo(dormitory_combo.currentData(), floor_combo)
        )
        layout.addWidget(floor_label)
        layout.addWidget(floor_combo)

        # Добавление этажа
        add_floor_button = QPushButton("Добавить этаж")
        add_floor_button.clicked.connect(lambda: self.add_floor(dormitory_combo.currentData(), floor_combo))
        layout.addWidget(add_floor_button)

        # Управление комнатами
        room_label = QLabel("Выберите тип комнаты и количество мест:")
        room_type_combo = QComboBox()
        room_type_combo.addItems(["Мужская", "Женская", "Семейная"])
        bed_count_input = QLineEdit()
        bed_count_input.setPlaceholderText("Количество мест")
        layout.addWidget(room_label)
        layout.addWidget(room_type_combo)
        layout.addWidget(bed_count_input)

        add_room_button = QPushButton("Добавить комнату")
        add_room_button.clicked.connect(
            lambda: self.add_room(floor_combo.currentData(), room_type_combo.currentText(), bed_count_input.text())
        )
        layout.addWidget(add_room_button)

        # Удаление комнаты
        remove_room_button = QPushButton("Удалить комнату")
        remove_room_button.clicked.connect(lambda: self.remove_room(floor_combo.currentData()))
        layout.addWidget(remove_room_button)

        self.tabs.addTab(widget, "Управление общежитием")
        self.tabs.setCurrentWidget(widget)

    def populate_dormitory_combo(self, combo):
        response = requests.get("http://localhost:8000/api/dormitories/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            dormitories = response.json()
            combo.clear()
            for dorm in dormitories:
                combo.addItem(dorm["name"], dorm["id"])

            if dormitories:
                combo.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить общежития")

    def populate_floor_combo(self, dormitory_id, combo):
        response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{dormitory_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            floors = response.json()
            combo.clear()
            for floor in floors:
                combo.addItem(f"Этаж {floor['floor_number']}", floor["id"])
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить этажи")

    def add_floor(self, dormitory_id, floor_combo):
        response = requests.get(f"http://localhost:8000/api/floors/by_dormitory/{dormitory_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            floors = response.json()
            next_floor_number = max([floor["floor_number"] for floor in floors]) + 1 if floors else 1
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить этажи")
            return

        data = {"dormitory_id": dormitory_id, "floor_number": next_floor_number}
        response = requests.post("http://localhost:8000/api/floors/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            self.populate_floor_combo(dormitory_id, floor_combo)
            QMessageBox.information(self, "Успех", f"Этаж {next_floor_number} добавлен!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить этаж")

    def add_room(self, floor_id, room_type, bed_count):
        """
        Добавляет комнату с автоматической генерацией номера.
        """
        try:
            bed_count = int(bed_count)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Количество мест должно быть числом")
            return

        # Получение следующего номера комнаты
        response = requests.get(f"http://localhost:8000/api/rooms/by_floor/{floor_id}",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            rooms = response.json()
            next_room_number = max([room['room_number'] for room in rooms], default=0) + 1
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить комнаты")
            return

        # Отправка данных
        data = {
            "floor_id": floor_id,
            "room_type": room_type.lower(),  # Тип комнаты на английском
            "room_number": next_room_number,
            "bed_count": bed_count
        }
        response = requests.post("http://localhost:8000/api/rooms/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Успех", f"Комната {next_room_number} добавлена!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить комнату")

    def remove_room(self, floor_id):
        room_combo = QComboBox()
        self.populate_room_combo(floor_id, room_combo)

        def confirm_removal():
            room_id = room_combo.currentData()
            response = requests.delete(f"http://localhost:8000/api/rooms/{room_id}",
                                       headers={"Authorization": f"Bearer {self.token}"})
            if response.status_code == 200:
                QMessageBox.information(self, "Успех", "Комната удалена!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить комнату")

        dialog = QWidget()
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Выберите комнату для удаления:"))
        layout.addWidget(room_combo)
        remove_button = QPushButton("Удалить")
        remove_button.clicked.connect(confirm_removal)
        layout.addWidget(remove_button)
        dialog.setWindowTitle("Удаление комнаты")
        dialog.show()

    def setup_students_tab(self):
        layout = QVBoxLayout(self.students_tab)

        # Таблица для отображения студентов
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(5)
        self.students_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Курс", "Группа", "Иногородний"])
        layout.addWidget(self.students_table)

        # Управляющая кнопка
        add_student_button = QPushButton("Добавить студента")
        add_student_button.clicked.connect(self.add_student_widget)
        layout.addWidget(add_student_button)




        self.load_students()

        self.load_students()


    def setup_staff_tab(self):
        layout = QVBoxLayout(self.staff_tab)

        # Таблица для отображения персонала
        self.staff_table = QTableWidget()
        self.staff_table.setColumnCount(3)
        self.staff_table.setHorizontalHeaderLabels(["Имя", "Фамилия", "Контакты"])
        layout.addWidget(self.staff_table)

        # Управляющая кнопка
        add_staff_button = QPushButton("Добавить работника деканата")
        add_staff_button.clicked.connect(self.add_staff_widget)
        layout.addWidget(add_staff_button)

        self.load_staff()

    def setup_violations_tab(self):
        layout = QVBoxLayout(self.violations_tab)

        # Таблица для отображения нарушений
        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(3)
        self.violations_table.setHorizontalHeaderLabels(["Студент", "Описание", "Дата"])
        layout.addWidget(self.violations_table)

        # Управляющая кнопка
        add_violation_button = QPushButton("Добавить нарушение")
        add_violation_button.clicked.connect(self.add_violation_widget)
        layout.addWidget(add_violation_button)

        self.load_violations()

    # Методы загрузки данных
    def load_dormitories(self):
        response = requests.get("http://localhost:8000/api/dormitories/", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            dormitories = response.json()
            self.dormitories_table.setRowCount(len(dormitories))
            for i, dorm in enumerate(dormitories):
                self.dormitories_table.setItem(i, 0, QTableWidgetItem(dorm["name"]))
                self.dormitories_table.setItem(i, 1, QTableWidgetItem(dorm["address"]))
                self.dormitories_table.setItem(i, 2, QTableWidgetItem(dorm["description"]))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить список общежитий")

    def load_students(self):
        response = requests.get("http://localhost:8000/api/students/", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            students = response.json()
            self.students_table.setRowCount(len(students))
            for i, student in enumerate(students):
                self.students_table.setItem(i, 0, QTableWidgetItem(student["first_name"]))
                self.students_table.setItem(i, 1, QTableWidgetItem(student["last_name"]))
                self.students_table.setItem(i, 2, QTableWidgetItem(str(student["course"])))
                self.students_table.setItem(i, 3, QTableWidgetItem(str(student["grup"])))
                self.students_table.setItem(i, 4, QTableWidgetItem("Да" if student["is_non_local"] else "Нет"))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить список студентов")

    def load_staff(self):
        response = requests.get("http://localhost:8000/api/deanery_staff/", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            staff = response.json()
            self.staff_table.setRowCount(len(staff))
            for i, member in enumerate(staff):
                self.staff_table.setItem(i, 0, QTableWidgetItem(member["first_name"]))
                self.staff_table.setItem(i, 1, QTableWidgetItem(member["last_name"]))
                self.staff_table.setItem(i, 2, QTableWidgetItem(member["contact_info"]))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить список сотрудников")

    def load_violations(self):
        response = requests.get("http://localhost:8000/api/violations/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            violations = response.json()
            self.violations_table.setRowCount(len(violations))
            for i, violation in enumerate(violations):
                student_response = requests.get(f"http://localhost:8000/api/students/{violation['student_id']}",
                                                headers={"Authorization": f"Bearer {self.token}"})
                if student_response.status_code == 200:
                    student = student_response.json()
                    student_info = f"{student['first_name']} {student['last_name']} (Группа: {student['grup']})"
                    self.violations_table.setItem(i, 0, QTableWidgetItem(student_info))
                else:
                    self.violations_table.setItem(i, 0, QTableWidgetItem("Неизвестный студент"))
                self.violations_table.setItem(i, 1, QTableWidgetItem(violation["description"]))
                self.violations_table.setItem(i, 2, QTableWidgetItem(violation["violation_date"]))
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить список нарушений")

    # Методы добавления данных
    def add_dormitory_widget(self):
        self.add_form_widget("Добавить общежитие", ["Название", "Адрес", "Описание"], self.add_dormitory)

    def add_student_widget(self):
        self.add_form_widget("Добавить студента",
                             ["Имя", "Фамилия", "Дата рождения", "Контакты", "Курс", "Группа", "Иногородний", "Пароль",
                              "Пол"], self.add_student)

    def populate_student_combo(self, combo):
        response = requests.get("http://localhost:8000/api/students/",
                                headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            students = response.json()
            for student in students:
                combo.addItem(f"{student['first_name']} {student['last_name']} (Group {student['grup']})",
                              student['id'])
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить список студентов")



    def add_staff_widget(self):
        self.add_form_widget("Добавить работника деканата", ["Имя", "Фамилия", "Контакты", "Пароль"], self.add_staff)

    def add_violation_widget(self):
        self.add_form_widget("Добавить нарушение", ["Студент", "Описание", "Дата"], self.add_violation)

    def add_form_widget(self, title, fields, submit_function):
        form_layout = QVBoxLayout()
        inputs = {}
        for field in fields:
            label = QLabel(field)
            if field == "Дата" or field == "Дата рождения":
                input_widget = QDateEdit()
                input_widget.setCalendarPopup(True)
            elif field == "Студент":
                input_widget = QComboBox()
                self.populate_student_combo(input_widget)
            elif field == "Общежитие":
                input_widget = QComboBox()
                self.populate_dormitory_combo(input_widget)
            elif field == "Пол":
                input_widget = QComboBox()
                input_widget.addItems(["Мужской", "Женский"])
            elif field == "Иногородний":
                input_widget = QCheckBox()
            else:
                input_widget = QLineEdit()
            form_layout.addWidget(label)
            form_layout.addWidget(input_widget)
            inputs[field] = input_widget
        submit_button = QPushButton("Сохранить")
        submit_button.clicked.connect(lambda: submit_function(inputs))
        form_layout.addWidget(submit_button)

        widget = QWidget()
        widget.setLayout(form_layout)
        self.tabs.addTab(widget, title)

        # Включение кнопки закрытия для новой вкладки
        self.tabs.setCurrentWidget(widget)


    def add_dormitory(self, inputs):
        data = {
            "name": inputs["Название"].text(),
            "address": inputs["Адрес"].text(),
            "description": inputs["Описание"].text()
        }
        response = requests.post("http://localhost:8000/api/dormitories/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Успех", "Общежитие добавлено!")
            self.load_dormitories()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить общежитие")

    def add_student(self, inputs):
        gender_mapping = {
            "Мужской": "male",
            "Женский": "female"
        }
        data = {
            "first_name": inputs["Имя"].text(),
            "last_name": inputs["Фамилия"].text(),
            "birth_date": inputs["Дата рождения"].date().toString("yyyy-MM-dd"),
            "contact_info": inputs["Контакты"].text(),
            "course": int(inputs["Курс"].text()),
            "grup": int(inputs["Группа"].text()),
            "is_non_local": inputs["Иногородний"].isChecked(),
            "password": inputs["Пароль"].text(),
            "gender": gender_mapping[inputs["Пол"].currentText()]
        }
        response = requests.post("http://localhost:8000/api/students/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Успех", "Студент добавлен!")
            self.load_students()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить студента")

    def add_staff(self, inputs):
        staff_data = {
            "first_name": inputs["Имя"].text(),
            "last_name": inputs["Фамилия"].text(),
            "contact_info": inputs["Контакты"].text(),
            "password": inputs["Пароль"].text()
        }
        response = requests.post("http://localhost:8000/api/deanery_staff/", json=staff_data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Добавление работника деканата", "Сотрудник успешно добавлен")
            self.load_staff()
        else:
            QMessageBox.warning(self, "Добавление работника деканата", "Не удалось добавить работника деканата")


    def add_violation(self, inputs):
        data = {
            "student_id": int(inputs["Студент"].currentData()),
            "description": inputs["Описание"].text(),
            "date": inputs["Дата"].date().toString("yyyy-MM-dd")
        }
        print(data)
        response = requests.post("http://localhost:8000/api/violations/", json=data,
                                 headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            QMessageBox.information(self, "Успех", "Нарушение добавлено!")
            self.load_violations()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить нарушение")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    token = "ваш_токен"  # Замените на реальный токен
    window = DeaneryStaffMainWindow(token)
    window.show()
    sys.exit(app.exec())
