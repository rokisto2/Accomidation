from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

from App.transferDesign.ui_mainWindow import Ui_MainWindow # Импортируйте сгенерированный файл напрямую

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.nextWindow)
        self.ui.pushButton_2.clicked.connect(self.close_window)

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