import math
from tkinter import filedialog
import PIL
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageOps


class ImageProcessing:

    def __init__(self):
        self.image = " "

    def open_image(self):
        filepath = filedialog.askopenfilename()
        self.image = Image.open(filepath)

        return

    def fft_for_rotate(self):
        #image = cv2.imread(filepath)
        # wyciąganie siatki i wykresu dla rotate
        image_hsv = cv2.cvtColor(np.array(self.image), cv2.COLOR_BGR2HSV)

        lower_range_red = np.array([140, 100, 100])
        upper_range_red = np.array([180, 255, 255])

        mask_grid = cv2.inRange(image_hsv, lower_range_red, upper_range_red)

        fft_grid = np.fft.fft2(mask_grid)
        magnitude_grid = np.abs(fft_grid)
        normalized_magnitude_grid = cv2.normalize(magnitude_grid, None, 0, 255, cv2.NORM_MINMAX)
        normalized_magnitude_grid_uint8 = normalized_magnitude_grid.astype(np.uint8)

        return normalized_magnitude_grid_uint8

    def rotate_chart(self, normalized_magnitude_grid_uint8):
        height, width = normalized_magnitude_grid_uint8.shape

        for x in range(width):
            for y in range(height):
                if normalized_magnitude_grid_uint8[y, x] > 50:
                    normalized_magnitude_grid_uint8[y, x] = 255
                else:
                    normalized_magnitude_grid_uint8[y, x] = 0

        pixels = np.argwhere(normalized_magnitude_grid_uint8 == 255)

        x1, y1 = pixels[2]
        x2, y2 = pixels[10]

        tan = (x1 - x2) / (y1 - y2)

        angle_radian = math.atan(tan)
        angle = math.degrees(angle_radian)

        rotate_img = self.image
        rotated_image = rotate_img.rotate(angle)

        return rotated_image

    def color_change_chart( self, rotated_image):
        rotated_image_rgb = rotated_image.convert("RGB")
        rotated_image_rgb = np.array(rotated_image_rgb)

        img_gray = cv2.cvtColor(np.array(rotated_image_rgb), cv2.COLOR_RGB2GRAY)

        # cv2.imshow('grayscale', img_gray)

        return img_gray, rotated_image_rgb

    def gaussian_filter(self, img_gray):
        # Otsu's thresholding after Gaussian filtering
        blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
        ret3, chart = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        median_filtered = cv2.medianBlur(chart, 3)

        return median_filtered

    def remove_isolated_pixels(self, chart_after_filter_1):
        chart_after_filter_1_pil = Image.fromarray(np.uint8(chart_after_filter_1))

        # Invert the colors of the PIL image
        chart_after_filter_np = PIL.ImageOps.invert(chart_after_filter_1_pil)

        # print (type(chart_after_filter_np))
        chart_after_filter = np.array(chart_after_filter_np)
        # load image, ensure binary, remove bar on the left

        kernel = np.ones((2, 2), np.uint8)
        img_erosion = cv2.erode(chart_after_filter, kernel, iterations=1)
        # cv2.imshow('erosion', img_erosion)

        img_erosion = cv2.threshold(img_erosion, 254, 255, cv2.THRESH_BINARY)[1]
        input_image_comp = cv2.bitwise_not(img_erosion)  # could just use 255-img

        kernel1 = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]], np.uint8)
        kernel2 = np.array([[1, 1, 1],
                            [1, 0, 1],
                            [1, 1, 1]], np.uint8)

        hitormiss1 = cv2.morphologyEx(img_erosion, cv2.MORPH_ERODE, kernel1)
        hitormiss2 = cv2.morphologyEx(input_image_comp, cv2.MORPH_ERODE, kernel2)
        hitormiss = cv2.bitwise_and(hitormiss1, hitormiss2)

        # cv2.imshow('isolated', hitormiss)

        hitormiss_comp = cv2.bitwise_not(hitormiss)  # could just use 255-img
        del_isolated = cv2.bitwise_and(img_erosion, img_erosion, mask=hitormiss_comp)
        # cv2.imshow('removed', del_isolated)

        return del_isolated



cv2.waitKey(0)
cv2.destroyAllWindows()