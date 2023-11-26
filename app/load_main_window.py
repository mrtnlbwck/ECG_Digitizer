from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication, QDialog
from PyQt5 import uic, QtWidgets
from image_processing import ImageProcessing
from load_scale_window import ScaleUI

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        import os
        print(os.getcwd())

        uic.loadUi("C:/Users/marty/Documents/GitHub/ECG_Digitizer/ui/main_window.ui", self)

        self.label = self.findChild(QLabel, "label")
        self.button = self.findChild(QPushButton, "pushButton")

        self.button.clicked.connect(self.click)

        self.image_processor = ImageProcessing()  # Instantiate ImageProcessing

        self.show()

    def openWindow(self, img_rgb, img_gray, chart_data):
        self.window = QDialog()
        self.scale_ui_window = ScaleUI(img_rgb, img_gray, chart_data)
        self.scale_ui_window.show()

    def click(self):
        self.image_processor.open_image()
        result = self.image_processor.fft_for_rotate()
        rotated_image = self.image_processor.rotate_chart(result)
        img_gray = self.image_processor.color_change_chart(rotated_image)[0]
        img_rgb = self.image_processor.color_change_chart(rotated_image)[1]
        chart_after_filter = self.image_processor.gaussian_filter(img_gray)
        chart_after_delete = self.image_processor.remove_isolated_pixels(chart_after_filter)
        self.openWindow(img_rgb, img_gray, chart_after_delete)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
