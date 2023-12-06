import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


class ImageProcessing:

    def color_change_chart(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)

        img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

        return img_gray, img_rgb
    def difference_of_gaussians(self, image):
        blur1 = cv2.GaussianBlur(image, (151, 151), 0)
        blur2 = cv2.GaussianBlur(image, (5, 5), 0)
        dog = cv2.absdiff(blur1, blur2)

        dog_gray = cv2.cvtColor(dog, cv2.COLOR_BGR2GRAY)
        _, binary_dog = cv2.threshold(dog_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary_dog = cv2.medianBlur(binary_dog, 3)

        return binary_dog

    def mean_image(self, image):
        grain = 30
        width, height = image.shape
        mean_image = np.empty((width - grain + 1, height - grain + 1))

        for k in range(width - grain + 1):
            for l in range(height - grain + 1):
                mean_image[k, l] = np.mean(image[k:k + grain, l:l + grain])

        return mean_image

    def imthreshold(self, imin):
        prog = 20
        xx, yy = imin.shape
        o = np.zeros((xx, yy), dtype=np.uint8)

        for k in range(xx):
            for l in range(yy):
                if imin[k, l] > prog:
                    o[k, l] = 1
                else:
                    o[k, l] = 0

        return o

    def multiply(self, dog_image, binary_image):
        grain = 30
        padding = grain // 2
        binary_image_padded = np.pad(binary_image, ((padding, padding), (padding, padding)), mode='constant')

        binary_image_padded_trimmed = binary_image_padded[:-1, :-1]

        result = np.multiply(dog_image, binary_image_padded_trimmed)

        return result

    def dividing(self, img):
        histogram_y = np.sum(img, axis=1)
        max_value = np.max(histogram_y)
        min_peak_height = max_value / 2

        # Set the minimum distance between peaks (adjust as needed)
        min_peak_distance = 10

        peaks, _ = find_peaks(histogram_y, height=min_peak_height, distance=min_peak_distance)


        distances = np.diff(peaks)
        half_distances = distances // 2

        medians = peaks[:-1] + half_distances

        return medians

    def cropping(self, medians, result_multiply):
        charts = []

        for i in range(len(medians) + 1):
            if i == 0:
                charts.append(result_multiply[:medians[i]])
            elif i == len(medians):
                charts.append(result_multiply[medians[i - 1]:])
            else:
                charts.append(result_multiply[medians[i - 1]:medians[i]])


        return charts

    def plot_cropped_charts(self, charts):
        for i, chart in enumerate(charts):
            plt.subplot(len(charts), 1, i + 1)
            plt.imshow(chart, cmap='gray')  # Assuming the charts are grayscale
            plt.title(f'Chart {i + 1}')
            plt.axis('off')

        plt.show()
