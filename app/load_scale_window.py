import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QDialog
from PyQt5 import uic, QtWidgets, QtCore
import sys

from app.data_processing import DataProcessing
from app.pixels_processing import PixelsProcessing
from image_processing import ImageProcessing  # Assuming this import is necessary


class ScaleUI(QDialog):
    def __init__(self, img_rgb, img_gray, chart_data):
        super(ScaleUI, self).__init__()

        uic.loadUi("C:/Users/marty/Documents/GitHub/ECG_Digitizer/ui/scale_window.ui", self)

        self.label_speed = self.findChild(QLabel, "label_speed")
        self.label_volt = self.findChild(QLabel, "label_volt")
        self.label_s = self.findChild(QLabel, "label_s")
        self.label_mV = self.findChild(QLabel, "label_mV")
        self.button = self.findChild(QPushButton, "pushButton")

        self.button.clicked.connect(self.click)

        self.image_processor = ImageProcessing()  # Instantiate ImageProcessing

        self.reference_points = []
        self.scale_x = None
        self.scale_y = None
        self.end_of_clicking = False
        self.pixels_processor = PixelsProcessing()
        self.data_processor = DataProcessing()

        self.img_gray = img_gray
        self.img_rgb = img_rgb
        self.chart_after_delete = chart_data

        self.show()

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

                self.scale_x = 5/(x_mm*pixel_distance_x)
                self.scale_y = pixel_distance_y / (5 * y_mm)

                print(self.scale_x, self.scale_y)

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

    # def openWindow(self, scale_x, scale_y, img_gray, chart_data):
    #     self.window = QtWidgets.QDialog()
    #     self.ui = Ui_result()
    #     self.ui.setupUi(self.window, scale_x, scale_y, img_gray, chart_data)
    #     self.window.show()

    def click(self):
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

    ui = ScaleUI()
    img_rgb = ui.img_rgb
    img_gray = ui.img_gray
    chart_data = ui.chart_after_delete

    pixels_processor = PixelsProcessing()
    data_processor = DataProcessing()

    scale_window.show()

    sys.exit(app.exec_())
