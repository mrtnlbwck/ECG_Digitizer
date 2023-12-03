import cv2
import numpy as np


class ImageProcessing:

    def open_image(self, filepath):
        image = cv2.imread(filepath)

        return image

    def color_change_chart(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)

        img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

        return img_gray, img_rgb

    def filtering(self, ekg_image):
        ekg_image[:3, :] = 255  # Górna krawędź
        ekg_image[-3:, :] = 255  # Dolna krawędź
        ekg_image[:, :3] = 255  # Lewa krawędź
        ekg_image[:, -3:] = 255  # Prawa krawędź

        _, binary_image = cv2.threshold(ekg_image, 133, 255, cv2.THRESH_BINARY)

       # cv2.imshow('binary', binary_image)

        filtered_image = cv2.medianBlur(binary_image, 3)

        kernel_opening = np.ones((5, 5), np.uint8)
        opened_edges = cv2.morphologyEx(filtered_image, cv2.MORPH_OPEN, kernel_opening)

       #0 cv2.imshow('filtered', opened_edges)

        print('sixze', opened_edges.shape)

        return opened_edges


