from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

from App.transferDesign.ui_mainWindow import Ui_MainWindow # Импортируйте сгенерированный файл напрямую

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.inactivity_timer = QTimer(self)
        self.inactivity_timer.timeout.connect(self.close_window)
        self.inactivity_timer.start(60000)  # 1 minute (60000 ms)

        # Connect user interaction signals to reset the timer
        self.ui.pushButton.clicked.connect(self.reset_timer)
        self.ui.pushButton_2.clicked.connect(self.reset_timer)

        self.ui.pushButton.clicked.connect(self.nextWindow)
        self.ui.pushButton_2.clicked.connect(self.close_window)

    def reset_timer(self):
        self.inactivity_timer.start(60000)

    def nextWindow(self):
        from App.Interfice.Login import LoginWindow
        self.loginWindow = LoginWindow()
        self.loginWindow.show()
        self.close()

    def close_window(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())