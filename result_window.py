# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from data_processing import DataProcessing
from pixels_processing import PixelsProcessing


class Ui_result(object):

    def setupUi(self, result_window, scale_x, scale_y, img_gray, chart_data):
        result_window.setObjectName("Scale Window")
        result_window.resize(454, 190)
        self.buttonBox = QtWidgets.QDialogButtonBox(result_window)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.img_gray = img_gray
        self.chart_after_delete = chart_data
        self.result_window_button = QtWidgets.QPushButton(result_window)
        self.result_window_button.setGeometry(QtCore.QRect(140, 120, 171, 51))
        self.result_window_button.setObjectName("scale_button")
        self.result_window_button.clicked.connect(self.clicked)
        self.label = QtWidgets.QLabel(result_window)
        self.label.setGeometry(QtCore.QRect(30, 30, 241, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(result_window)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 241, 16))
        self.label_2.setObjectName("label_2")
        self.retranslateUi(result_window)
        QtCore.QMetaObject.connectSlotsByName(result_window)

    def retranslateUi(self, result_window):
        _translate = QtCore.QCoreApplication.translate
        result_window.setWindowTitle(_translate("result_window", "Wyniki"))
        self.result_window_button.setText(_translate("result", "ZATWIERDŹ"))
        self.label.setText(_translate("result_window", str(self.scale_x)))
        self.label_2.setText(_translate("result_window", str(self.scale_y)))

    def clicked(self):
        pixels = pixels_processor.put_into_pixels(chart_data)
        pixels_final = pixels_processor.process_and_visualize_data(pixels, img_gray)
        sorted_data = data_processor.sorting(pixels_final)
        xy = data_processor.extract_xy(sorted_data)
        mean_xy = data_processor.mean_chart(*xy)
        scaled_xy = data_processor.scale(*mean_xy, scale_x, scale_y)
        data_processor.spline(*scaled_xy)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    result_window = QtWidgets.QDialog()

    ui = Ui_result()
    scale_x = ui.scale_x
    scale_y = ui.scale_y
    img_gray = ui.img_gray
    chart_data = ui.chart_after_delete

    ui.setupUi(result_window, scale_x, scale_y, img_gray, chart_data)
    pixels_processor = PixelsProcessing()
    data_processor = DataProcessing()
    result_window.show()



    sys.exit(app.exec_())
