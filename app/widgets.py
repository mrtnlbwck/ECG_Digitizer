from copy import deepcopy

import cv2
import numpy as np
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Adjust(QWidget):
    def __init__(self, main):
        super().__init__()
        uic.loadUi("../ui/adjust_image.ui", self)
        self.get_zoom_factor = main.get_zoom_factor

        self.img_class, self.update_img, self.base_frame = main.img_class, main.update_img, main.base_frame
        self.rb, self.vbox, self.flip, self.zoom_factor = main.rb, main.vbox, main.flip, main.zoom_factor
        self.zoom_moment, self.slider, self.gv, self.vbox1 = main.zoom_moment, main.slider, main.gv, main.vbox1
        self.start_detect = False

        self.frame = self.findChild(QFrame, "frame")
        self.crop_btn = self.findChild(QPushButton, "crop_btn")
        self.rotate_btn = self.findChild(QPushButton, "rotate_btn")

        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("../icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(60, 60))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("../icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(60, 60))

        self.y_btn.clicked.connect(lambda _: self.click_y())
        self.n_btn.clicked.connect(lambda _: self.click_n())
        self.crop_btn.clicked.connect(lambda _: self.click_crop())
        self.rotate_btn.clicked.connect(lambda _: self.click_crop(rotate=True))

    def click_crop(self, rotate=False):
        def click_y1():
            self.rb.update_dim()
            if rotate:
                self.img_class.rotate_img(self.rotate_value, crop=True, flip=self.flip)
                self.img_class.crop_img(int(self.rb.top * 2 / self.zoom_factor),
                                        int(self.rb.bottom * 2 / self.zoom_factor),
                                        int(self.rb.left * 2 / self.zoom_factor),
                                        int(self.rb.right * 2 / self.zoom_factor))
            else:
                self.img_class.reset(self.flip)
                self.img_class.crop_img(int(self.rb.top / self.zoom_factor), int(self.rb.bottom / self.zoom_factor),
                                        int(self.rb.left // self.zoom_factor), int(self.rb.right // self.zoom_factor))

            self.update_img()
            self.zoom_moment = False

            self.img_class.img_copy = deepcopy(self.img_class.img)
            self.slider.setParent(None)
            self.slider.valueChanged.disconnect()
            crop_frame.frame.setParent(None)
            self.vbox.addWidget(self.frame)
            self.rb.close()

        def click_n1():
            if not np.array_equal(img_copy, self.img_class.img):
                msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                           QMessageBox.Yes | QMessageBox.No)
                if msg != QMessageBox.Yes:
                    return False

            self.img_class.reset()
            self.update_img()
            self.zoom_moment = False

            self.slider.setParent(None)
            self.slider.valueChanged.disconnect()
            crop_frame.frame.setParent(None)
            self.vbox.addWidget(self.frame)
            self.rb.close()

        def change_slide():
            self.rotate_value = self.slider.value()
            self.slider.setValue(self.rotate_value)

            self.img_class.rotate_img(self.rotate_value)

            self.rb.setGeometry(int(self.img_class.left * self.zoom_factor), int(self.img_class.top * self.zoom_factor),
                                int((self.img_class.right - self.img_class.left) * self.zoom_factor),
                                int((self.img_class.bottom - self.img_class.top) * self.zoom_factor))

            self.rb.update_dim()
            self.update_img(True)

        crop_frame = Crop()
        crop_frame.n_btn.clicked.connect(click_n1)
        crop_frame.y_btn.clicked.connect(click_y1)
        self.flip = [False, False]

        self.frame.setParent(None)
        self.vbox.addWidget(crop_frame.frame)
        self.zoom_factor = self.get_zoom_factor()

        self.rb = ResizableRubberBand(self)
        self.rb.setGeometry(0, 0, int(self.img_class.img.shape[1] * self.zoom_factor),
                            int(self.img_class.img.shape[0] * self.zoom_factor))
        self.img_class.change_b_c(beta=-40)
        self.slider.valueChanged.connect(change_slide)

        if not rotate:
            self.update_img()
        else:
            self.vbox1.insertWidget(1, self.slider)
            self.slider.setRange(0, 360)
            self.slider.setValue(0)
            self.zoom_moment = True
            self.img_class.rotate_img(0)
            self.rb.setGeometry(0, 0, int(self.img_class.img.shape[1] * self.zoom_factor),
                                int(self.img_class.img.shape[0] * self.zoom_factor))
            self.update_img(True)

        img_copy = deepcopy(self.img_class.img)

    def click_y(self):
        self.start_detect = False
        self.frame.setParent(None)
        self.img_class.img_copy = deepcopy(self.img_class.img)
        self.img_class.grand_img_copy = deepcopy(self.img_class.img)
        self.vbox.addWidget(self.base_frame)

    def click_n(self):
        if not np.array_equal(self.img_class.grand_img_copy, self.img_class.img):
            msg = QMessageBox.question(self, "Cancel edits", "Confirm to discard all the changes?   ",
                                       QMessageBox.Yes | QMessageBox.No)
            if msg != QMessageBox.Yes:
                return False

        self.start_detect = False
        self.frame.setParent(None)
        self.img_class.grand_reset()
        self.update_img()
        self.vbox.addWidget(self.base_frame)


class Crop(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("../ui/crop.ui", self)

        self.frame = self.findChild(QFrame, "frame")
        self.y_btn = self.findChild(QPushButton, "y_btn")
        self.y_btn.setIcon(QIcon("../icon/check.png"))
        self.y_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.y_btn.setIconSize(QSize(70, 70))
        self.n_btn = self.findChild(QPushButton, "n_btn")
        self.n_btn.setIcon(QIcon("../icon/cross.png"))
        self.n_btn.setStyleSheet("QPushButton{border: 0px solid;}")
        self.n_btn.setIconSize(QSize(70, 70))


class ResizableRubberBand(QWidget):
    def __init__(self, main):
        super(ResizableRubberBand, self).__init__(main.gv)
        self.get_zoom_factor = main.get_zoom_factor

        self.img_class, self.update, self.zoom_factor = main.img_class, main.update, main.zoom_factor
        self.draggable, self.mousePressPos, self.mouseMovePos = True, None, None
        self.left, self.right, self.top, self.bottom = None, None, None, None
        self.borderRadius = 0

        self.setWindowFlags(Qt.SubWindow)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignRight | Qt.AlignBottom)

        self._band = QRubberBand(QRubberBand.Rectangle, self)
        self._band.show()
        self.show()

    def update_dim(self):
        self.left, self.top = self.pos().x(), self.pos().y()
        self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top

    def resizeEvent(self, event):
        try:
            self.left, self.top = self.pos().x(), self.pos().y()
            self.right, self.bottom = self._band.width() + self.left, self._band.height() + self.top
        except:
            pass
        self._band.resize(self.size())


