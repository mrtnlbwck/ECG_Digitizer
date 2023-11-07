# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from image_processing import ImageProcessing
from scale_window import Ui_scale


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(829, 395)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(290, 260, 241, 71))
        self.button.setObjectName("button")
        self.button.clicked.connect(self.clicked)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 70, 55, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digitalizacja EKG"))
        self.button.setText(_translate("MainWindow", "Wgraj obraz"))
        self.label.setText(_translate("MainWindow", "Wgraj obraz EKG hihi"))

    def openWindow(self, img_rgb, img_gray, chart_data):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_scale()
        self.ui.setupUi(self.window, img_rgb, img_gray, chart_data)
        self.window.show()

    def clicked(self):
        image_processor.open_image()
        result = image_processor.fft_for_rotate()
        rotated_image = image_processor.rotate_chart(result)
        img_gray = image_processor.color_change_chart(rotated_image)[0]
        img_rgb = image_processor.color_change_chart(rotated_image)[1]
        chart_after_filter = image_processor.gaussian_filter(img_gray)
        chart_after_delete = image_processor.remove_isolated_pixels(chart_after_filter)
        self.openWindow(img_rgb, img_gray, chart_after_delete)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    image_processor = ImageProcessing()

    sys.exit(app.exec_())
