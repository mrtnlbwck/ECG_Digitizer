import numpy as np


class PixelsProcessing:
    def put_into_pixels(self, chart_after_filter):
        pixels = np.argwhere(chart_after_filter == 255)

        return pixels