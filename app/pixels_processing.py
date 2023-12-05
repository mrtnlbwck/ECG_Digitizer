import numpy as np
from scipy import ndimage


class PixelsProcessing:
    def put_into_pixels(self, chart_after_filter):
        pixels = np.argwhere(chart_after_filter == 0)

        return pixels