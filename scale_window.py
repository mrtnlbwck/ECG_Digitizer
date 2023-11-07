# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from data_processing import DataProcessing
from pixels_processing import PixelsProcessing
from result_window import Ui_result


class Ui_scale(object):
    def __init__(self):
        self.reference_points = []
        self.scale_x = None
        self.scale_y = None
        self.end_of_clicking = False
        self.pixels_processor = PixelsProcessing()
        self.data_processor = DataProcessing()

    def setupUi(self, scale_window, img_rgb, img_gray, chart_data):
        self.img_gray = img_gray
        self.img_rgb = img_rgb
        self.chart_after_delete = chart_data
        scale_window.setObjectName("Scale Window")
        scale_window.resize(454, 190)
        self.buttonBox = QtWidgets.QDialogButtonBox(scale_window)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.textEdit = QtWidgets.QTextEdit(scale_window)
        self.textEdit.setGeometry(QtCore.QRect(280, 20, 91, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(scale_window)
        self.textEdit_2.setGeometry(QtCore.QRect(280, 60, 91, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.scale_window_button = QtWidgets.QPushButton(scale_window)
        self.scale_window_button.setGeometry(QtCore.QRect(140, 120, 171, 51))
        self.scale_window_button.setObjectName("scale_button")
        self.scale_window_button.clicked.connect(self.on_submit_clicked)
        self.label = QtWidgets.QLabel(scale_window)
        self.label.setGeometry(QtCore.QRect(30, 30, 241, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(scale_window)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 241, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(scale_window)
        self.label_3.setGeometry(QtCore.QRect(380, 30, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(scale_window)
        self.label_4.setGeometry(QtCore.QRect(380, 70, 55, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(scale_window)
        self.buttonBox.accepted.connect(scale_window.accept)  # type: ignore
        self.buttonBox.rejected.connect(scale_window.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(scale_window)

    def retranslateUi(self, scale_window):
        _translate = QtCore.QCoreApplication.translate
        scale_window.setWindowTitle(_translate("scale_window", "Wprowadź wartości do przeliczenia skali"))
        self.scale_window_button.setText(_translate("scale", "ZATWIERDŹ"))
        self.label.setText(_translate("scale_window", "Wprowadź szybkość przesuwu zapisu: "))
        self.label_2.setText(_translate("scale_window", "Wprowadź wartość potencjału:"))
        self.label_3.setText(_translate("scale_window", "mm/s"))
        self.label_4.setText(_translate("scale_window", "mm/mV"))

    def calculate_pixel_distance(self, point1, point2):
        return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def on_mouse(self, event, x, y, flags, params):
        callback_params = params
        image = callback_params["img_rgb"]
        x_mm = callback_params["value1"]
        y_mm = callback_params["value2"]
        _translate = QtCore.QCoreApplication.translate
        # x_mm = 10
        # y_mm = 10
        # x_mm = None
        # y_mm = None

        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.reference_points) < 2:
                # x_mm = input("Wprowadź ...x w [mm/sec] ")
                self.reference_points.append((x, y))
                cv2.circle(image, (x, y), 2, (0, 0, 255), -1)  # Rysuj czerwone kółko w zaznaczonym punkcie
                cv2.putText(image, 'x', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            elif len(self.reference_points) < 4:
                # y_mm = input("Wprowadź ...y w [mV/sec] ")
                self.reference_points.append((x, y))
                cv2.circle(image, (x, y), 2, (255, 0, 0), -1)  # Rysuj czerwone kółko w zaznaczonym punkcie
                cv2.putText(image, 'y', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            # Oblicz odległość między punktami referencyjnymi
            if len(self.reference_points) == 4:
                pixel_distance_x = self.calculate_pixel_distance(self.reference_points[-4], self.reference_points[-3])
                pixel_distance_y = self.calculate_pixel_distance(self.reference_points[-2], self.reference_points[-1])

                self.scale_x = x_mm / (2 * pixel_distance_x)
                self.scale_y = y_mm / (2 * pixel_distance_y)

                self.end_of_clicking = True

                if self.end_of_clicking:
                    cv2.destroyAllWindows()
                    #self.openWindow(self.scale_x, self.scale_y, self.img_gray, self.chart_after_delete)
                    pixels = self.pixels_processor.put_into_pixels(self.chart_after_delete)
                    pixels_final = self.pixels_processor.process_and_visualize_data(pixels, self.img_gray)
                    sorted_data = self.data_processor.sorting(pixels_final)
                    xy = self.data_processor.extract_xy(sorted_data)
                    mean_xy = self.data_processor.mean_chart(*xy)
                    scaled_xy = self.data_processor.scale(*mean_xy, self.scale_x, self.scale_y)
                    self.data_processor.spline(*scaled_xy)


        if event == cv2.EVENT_MOUSEMOVE:
            zoom_factor = 3
            zoomed_image = image[max(0, y - 30): min(image.shape[0], y + 30),
                           max(0, x - 30): min(image.shape[1], x + 30)]
            zoomed_image = cv2.resize(zoomed_image, None, fx=zoom_factor, fy=zoom_factor)

            # Draw cursor on zoomed image
            cursor_color = (0, 255, 0)  # Green color for cursor
            cv2.drawMarker(zoomed_image, (zoomed_image.shape[1] // 2, zoomed_image.shape[0] // 2),
                           cursor_color, cv2.MARKER_CROSS, markerSize=15, thickness=2)
            cv2.imshow("Zoomed Image", zoomed_image)

    def openWindow(self, scale_x, scale_y, img_gray, chart_data):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_result()
        self.ui.setupUi(self.window, scale_x, scale_y, img_gray, chart_data)
        self.window.show()

    def on_submit_clicked(self):
        # Obsługa przycisku "ZATWIERDŹ"
        value1 = int(self.textEdit.toPlainText())  # Wartość z pierwszego pola tekstowego
        value2 = int(self.textEdit_2.toPlainText())

        callback_params = {"img_rgb": self.img_rgb, "value1": value1, "value2": value2}

        cv2.imshow("Image", self.img_rgb)
        cv2.setMouseCallback("Image", self.on_mouse, callback_params)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    scale_window = QtWidgets.QDialog()

    ui = Ui_scale()
    img_rgb = ui.img_rgb
    img_gray = ui.img_gray
    chart_data = ui.chart_after_delete
    ui.setupUi(scale_window, img_rgb, img_gray, chart_data)

    pixels_processor = PixelsProcessing()
    data_processor = DataProcessing()

    scale_window.show()

    sys.exit(app.exec_())
