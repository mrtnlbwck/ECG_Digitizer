import pathlib

import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QDialog, QWidget, QTextEdit
from PyQt5 import uic, QtWidgets, QtCore
import sys



class ChangeUI(QDialog):
    def __init__(self):
        super(ChangeUI, self).__init__()
        print("ScaleUI initialized")  # Add this line
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\..\\ui\\scale_window.ui", self)

        self.label_speed = self.findChild(QLabel, "label_speed")
        self.label_volt = self.findChild(QLabel, "label_volt")
        self.label_s = self.findChild(QLabel, "label_s")
        self.label_mV = self.findChild(QLabel, "label_mV")
        self.button = self.findChild(QPushButton, "button")
        self.text_speed = self.findChild(QTextEdit, "text_speed")
        self.text_volt = self.findChild(QTextEdit, "text_volt")

        self.speed_value = None
        self.volt_value = None


        self.button.clicked.connect(self.click)

    def click(self):
        self.speed_value = int(self.text_speed.toPlainText())
        self.volt_value = int(self.text_volt.toPlainText())

        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = ChangeUI()
    sys.exit(app.exec_())
