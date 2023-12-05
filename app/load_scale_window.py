import pathlib
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QLabel, QPushButton, QDialog, QMessageBox, QLineEdit
from PyQt5 import uic, QtWidgets, QtCore
import sys


class ChangeUI(QDialog):
    valuesChanged = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super(ChangeUI, self).__init__()
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\..\\ui\\scale_window.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\..\\icon\\icon.png"))
        self.setWindowTitle("Enter ECG paper values")

        self.label_speed = self.findChild(QLabel, "label_speed")
        self.label_volt = self.findChild(QLabel, "label_volt")
        self.label_s = self.findChild(QLabel, "label_s")
        self.label_mV = self.findChild(QLabel, "label_mV")
        self.button = self.findChild(QPushButton, "button")
        self.text_speed = self.findChild(QLineEdit, "speed_text")
        self.text_volt = self.findChild(QLineEdit, "volt_text")

        reg_ex = QRegExp("[1-9]|[1-4][0-9]|50")
        input_validator = QRegExpValidator(reg_ex, self.text_speed)
        self.text_speed.setValidator(input_validator)
        self.text_volt.setValidator(input_validator)

        self.speed_value = None
        self.volt_value = None

        self.button.clicked.connect(self.click)

    def click(self):
        if self.text_speed.text() == '' or self.text_volt.text() == '':
            QMessageBox.warning(self, "Enter both values", "Please enter both values", QMessageBox.Ok)
        else:
            try:
                self.speed_value = int(self.text_speed.text())
                self.volt_value = int(self.text_volt.text())
                self.valuesChanged.emit(self.speed_value, self.volt_value)
                self.close()
            except ValueError:
                QMessageBox.warning(self, "Invalid input", "Please enter numeric values only", QMessageBox.Ok)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = ChangeUI()
    sys.exit(app.exec_())
