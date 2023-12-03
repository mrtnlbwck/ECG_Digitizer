import sys

import qimage2ndarray
from PyQt5.QtGui import QPixmap
from data_processing import DataProcessing
from load_scale_window import ChangeUI
from pixels_processing import PixelsProcessing
from scripts import Images
from image_processing import ImageProcessing
from widgets import *
import resources


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        self.files = None
        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\..\\ui\\main_window.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\..\\icon\\icon.png"))
        self.setWindowTitle("ECG Digitizer")

        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.click)
        self.image = None
        self.image_window = None

        self.show()

    def click(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose Image File", "",
                                                "Image Files (*.jpg *.png *.jpeg *.ico);;All Files (*)")

        if files:
            self.files = files
            self.close()
            self.image_window = ImageUI(self.files)
            self.image_window.show()


class ImageUI(QWidget):
    def __init__(self, files):
        super(ImageUI, self).__init__()

        uic.loadUi(f"{pathlib.Path(__file__).parent.absolute()}\\..\\ui\\image_window.ui", self)
        self.setWindowIcon(QIcon(f"{pathlib.Path(__file__).parent.absolute()}\\..\\icon\\icon.png"))
        self.setWindowTitle("ECG Digitizer")



        self.move(120, 100)
        self.img_list, self.rb = [], None
        for f in files:
            self.img_list.append(Images(f))
        self.img_id = 0
        self.img_class = self.img_list[self.img_id]
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))

        self.vbox = self.findChild(QVBoxLayout, "vbox")
        self.vbox1 = self.findChild(QVBoxLayout, "vbox1")

        self.base_frame = self.findChild(QFrame, "base_frame")

        self.adjust_btn = self.findChild(QPushButton, "adjust_btn")
        self.adjust_btn.clicked.connect(self.adjust_frame)

        self.save_btn = self.findChild(QPushButton, "save_btn")
        self.save_btn.clicked.connect(self.click_con)

        self.change_btn = self.findChild(QPushButton, "change_btn")
        self.change_btn.clicked.connect(self.click_change)

        self.save_btn = self.findChild(QPushButton, "back_btn")
        self.save_btn.clicked.connect(self.click_back)
        self.save_btn.clicked.connect(self.close)
        self.slider = self.findChild(QSlider, "slider")
        self.slider.setParent(None)

        self.ui = None
        self.main_window = None
        self.saved_image = None

        self.gv = self.findChild(QGraphicsView, "gv")
        self.scene = QGraphicsScene()
        self.scene_img = self.scene.addPixmap(self.img)
        self.gv.setScene(self.scene)

        self.zoom_moment = False
        self._zoom = 0

        self.flip = [False, False]
        self.zoom_factor = 1

        self.image_processor = ImageProcessing()
        self.pixels_processor = PixelsProcessing()
        self.data_processor = DataProcessing()

        self.img_rgb = None
        self.img_gray = None
        self.chart_after_filter = None

        self.reference_points = []
        self.scale_x = None
        self.scale_y = None
        self.end_of_clicking = False

        self.speed_value = 25
        self.volt_value = 10

    def update_img(self, movable=False):
        self.img = QPixmap(qimage2ndarray.array2qimage(cv2.cvtColor(self.img_class.img, cv2.COLOR_BGR2RGB)))
        self.scene.removeItem(self.scene_img)
        self.scene_img = self.scene.addPixmap(self.img)
        if movable:
            self.scene_img.setFlag(QGraphicsItem.ItemIsMovable)
        else:
            self.fitInView()

    def get_zoom_factor(self):
        return self.zoom_factor

    def adjust_frame(self):
        adjust_frame = Adjust(self)
        self.base_frame.setParent(None)
        self.vbox.addWidget(adjust_frame.frame)

    def click_con(self):
        self.saved_image = self.img_class.img  # Zapisz obraz do zmiennej
        self.img_gray, self.img_rgb = self.image_processor.color_change_chart(self.saved_image)
        self.chart_after_filter = self.image_processor.filtering(self.img_gray)

        QMessageBox.information(self, "Instruction", "Mark two points on the x-axis that form a segment of 5mm, "
                                                     "then two more points on the y-axis  ", QMessageBox.Ok)


        cv2.imshow("Image", self.img_rgb)

        cv2.setMouseCallback("Image", self.on_mouse)

        self.hide()



    def click_change(self):
        change_window = ChangeUI()
        change_window.valuesChanged.connect(self.handle_values_changed)

        change_window.exec()

    def open_saving_window(self):
        saving_frame = SaveUI()
        saving_frame.exec()


    def handle_values_changed(self, speed_value, volt_value):
        self.speed_value = speed_value
        self.volt_value = volt_value

    def click_back(self):
        self.ui = UI()

    def wheelEvent(self, event):
        if self.zoom_moment:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.gv.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def fitInView(self):
        rect = QRectF(self.img.rect())
        if not rect.isNull():
            self.gv.setSceneRect(rect)

            unity = self.gv.transform().mapRect(QRectF(0, 0, 1, 1))
            self.gv.scale(1 / unity.width(), 1 / unity.height())
            view_rect = self.gv.viewport().rect()
            scene_rect = self.gv.transform().mapRect(rect)
            factor = min(view_rect.width() / scene_rect.width(),
                         view_rect.height() / scene_rect.height())
            self.gv.scale(factor, factor)
            self._zoom = 0
            self.zoom_factor = factor

    def calculate_pixel_distance(self, point1, point2):
        return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def on_mouse(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.reference_points) < 2:
                self.reference_points.append((x, y))
                cv2.circle(self.img_rgb, (x, y), 2, (0, 0, 255), -1)
                cv2.putText(self.img_rgb, 'x', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            elif len(self.reference_points) < 4:
                self.reference_points.append((x, y))
                cv2.circle(self.img_rgb, (x, y), 2, (255, 0, 0), -1)
                cv2.putText(self.img_rgb, 'y', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            if len(self.reference_points) == 4:
                cv2.waitKey(500)
                pixel_distance_x = self.calculate_pixel_distance(self.reference_points[-4], self.reference_points[-3])
                pixel_distance_y = self.calculate_pixel_distance(self.reference_points[-2], self.reference_points[-1])
                self.scale_x = 5 / (pixel_distance_x * self.speed_value)
                self.scale_y = 5 / (pixel_distance_y * self.volt_value)

                self.end_of_clicking = True

                if self.end_of_clicking:
                    cv2.destroyAllWindows()

                    pixels = self.pixels_processor.put_into_pixels(self.chart_after_filter)
                    sorted_data = self.data_processor.sorting(pixels)
                    xy = self.data_processor.extract_xy(sorted_data)
                    scaled_xy = self.data_processor.scale(*xy, self.scale_x, self.scale_y)
                    mean_xy = self.data_processor.mean_chart(*scaled_xy)
                    spline_xy = self.data_processor.spline(*mean_xy)
                    self.reference_points.clear()
                    self.close()
                    self.open_saving_window()


        if event == cv2.EVENT_MOUSEMOVE:
            zoom_factor = 3
            zoomed_size = 80  # Adjust this size based on your preference

            # Calculate the region to crop from the original image
            crop_y_start = max(0, y - zoomed_size)
            crop_y_end = min(self.img_rgb.shape[0], y + zoomed_size)
            crop_x_start = max(0, x - zoomed_size)
            crop_x_end = min(self.img_rgb.shape[1], x + zoomed_size)

            # Adjust the cursor position in the zoomed image
            cursor_x = x - crop_x_start
            cursor_y = y - crop_y_start

            # Crop the region from the original image

            zoomed_image = self.img_rgb[crop_y_start:crop_y_end, crop_x_start:crop_x_end]
            zoomed_image = cv2.resize(zoomed_image, None, fx=zoom_factor, fy=zoom_factor)

            cursor_color = (0, 255, 0)  # Green color for cursor
            cv2.drawMarker(zoomed_image, (cursor_x * zoom_factor, cursor_y * zoom_factor),
                           cursor_color, cv2.MARKER_CROSS, markerSize=15, thickness=2)
            zoomed_text = "Move the cursor to explore the image"
            cv2.putText(zoomed_image, zoomed_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (60, 20, 220))

            cv2.imshow("Zoomed Image", zoomed_image)




def main():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
