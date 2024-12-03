from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

from App.transferDesign.ui_programmWindow  import Ui_MainWindow # Импортируйте сгенерированный файл напрямую

class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AboutWindow()
    window.show()

    sys.exit(app.exec())