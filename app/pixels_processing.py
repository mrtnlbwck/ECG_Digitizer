import numpy as np
from scipy import ndimage


class PixelsProcessing:
    def put_into_pixels(self, chart_after_filter):

        pixels = np.argwhere(chart_after_filter == 0)


        return pixels

    #nieuzywana
    def process_and_visualize_data(self, coordinates, img, size_threshold=120):
        shape = img.shape
        data = np.zeros(shape, dtype=int)
        for coord in coordinates:
            x, y = coord
            data[x, y] = 1

        # Identify connected components
        labeled_data, num_labels = ndimage.measurements.label(data)

        # Calculate the size of each connected component
        label_sizes = [(labeled_data == label).sum() for label in range(num_labels + 1)]

        # Remove small connected components
        for label, size in enumerate(label_sizes):
            if size < size_threshold:
                data[labeled_data == label] = 0

        new_coordinates = np.argwhere(data)



        return new_coordinates
