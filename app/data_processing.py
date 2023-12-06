import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pyedflib import FILETYPE_EDFPLUS
from scipy.interpolate import interp1d
import pyedflib
from datetime import datetime, date


class DataProcessing:
    def sorting(self, data):
        swapped_data = [[y, x] for x, y in data]

        data_sorted = sorted(swapped_data, key=lambda y: y[0])

        return data_sorted

    def extract_xy(self, data_sorted):
        x_values = [pair[0] for pair in data_sorted]
        y_values = [pair[1] for pair in data_sorted]

        max_y = max(y_values)

        for i in range(len(y_values)):
            y_values[i] = y_values[i] * (-1)
            y_values[i] += max_y

        return x_values, y_values

    def mean_chart(self, x, y):
        data = {'x': x, 'y': y}

        df = pd.DataFrame(data)

        average_y = df.groupby('x')['y'].mean().reset_index()

        new_y = np.array(average_y['y'])
        new_x = np.array(average_y['x'])

        return new_x, new_y

    def scale(self, x, y, scaling_factor_x, scaling_factor_y):
        offset_y = y[0]

        # Scale the x values
        scaled_x = [xi * scaling_factor_x for xi in x]

        # Scale the y values, and subtract the missing value to make the first value zero
        scaled_y = [(yi - offset_y) * scaling_factor_y for yi in y]

        for i in range(len(x)):
            x[i] = scaled_x[i]

        for j in range(len(y)):
            y[j] = scaled_y[j]

        return scaled_x, scaled_y

    def spline(self, x, y):
        x_interp = np.linspace(np.min(x), np.max(x), 250)
        y_linear = interp1d(x, y)

        y_interp = y_linear(x_interp)

        return x_interp, y_interp

    def spline_with_additional_points(self, x, y, additional_points=5000):
        x_interp = np.linspace(np.min(x), np.max(x), len(x) + additional_points)
        y_linear = interp1d(x, y)

        y_interp = y_linear(x_interp)

        # plt.plot(x_interp, y_interp, color='red', marker='o')
        # plt.title('EKG Plot')
        # plt.xlabel('Time [s]')
        # plt.ylabel('Voltage [mV]')
        # plt.show()

        return x_interp, y_interp

    # def export_to_edf(self, filename, header, x, y):
    #     num_channels = len(x)
    #     # print(x[0])
    #     # sample_rate = int(1 / np.mean(np.diff(x[0])))
    #     sample_rate = 38
    #
    #     f = pyedflib.EdfWriter(filename, num_channels, file_type=FILETYPE_EDFPLUS)
    #
    #     try:
    #         f.setStartdatetime(datetime.now())
    #
    #         ekg_channel_info = {
    #             'label': header,
    #             'dimension': 'mV',
    #             'sample_frequency': sample_rate,
    #             # 'physical_max': round(max(y[0]), 6),
    #             # 'physical_min': round(min(y[0]), 6)
    #         }
    #
    #         for channel_num in range(num_channels):
    #             f.setSignalHeader(edfsignal=channel_num, channel_info=ekg_channel_info)
    #
    #         ekg_data = y
    #         # ekg_data = ekg_data.reshape((1, -1))
    #
    #         f.writeSamples(ekg_data)
    #
    #     finally:
    #         f.close()



