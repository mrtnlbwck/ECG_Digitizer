import numpy as np
import pandas as pd
import pyedflib
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
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

        print(new_x, new_y)

        return new_x, new_y

    def scale(self, x, y, scaling_factor_x, scaling_factor_y):

        scaled_x = [xi * scaling_factor_x for xi in x]
        scaled_y = [yi * scaling_factor_y for yi in y]

        for i in range(len(x)):
            x[i] = scaled_x[i]

        for j in range(len(y)):
            y[j] = scaled_y[j]

        return scaled_x, scaled_y

    def spline(self, x, y):
        x_interp = np.linspace(np.min(x), np.max(x), 250)
        y_linear = interp1d(x, y)

        y_interp = y_linear(x_interp)

        plt.plot(x_interp, y_interp, color='red', marker='o')
        plt.title('EKG Plot')
        plt.show()

        print('x:', x_interp, 'y:', y_interp)

        return x_interp, y_interp

    def export_to_edf(self, filename, x, y):
        # Assume self.x and self.y contain your EKG data
        num_channels = 1  # Number of channels in your EKG data
        sample_rate = 250  # Adjust this based on your data's sampling rate

        # Create an EdfWriter
        f = pyedflib.EdfWriter(filename, num_channels, file_type=pyedflib.FILETYPE_EDFPLUS)

        # Set metadata, such as patient information and recording start time
        f.setStartdatetime(datetime.now())

        ekg_channel_info = {
            'label': 'ECG',
            'dimension': 'mV',
            'sample_frequency': sample_rate,
            'physical_max': 1,  # Adjust based on your data
            'physical_min': -1,  # Adjust based on your data
            'digital_max': 32767,
            'digital_min': -32768
        }
        f.setSignalHeader(edfsignal=0, channel_info=ekg_channel_info)
        # Write EKG data to the file

        # Convert the EKG data to int16 as required by EDF format
        #ekg_data = (y * 1e1).astype(np.int16)

        max_original_value = np.max(y)
        scaled_data = ((y / max_original_value) * 2048)

        # Convert to 16-bit integers
        ekg_data = np.round(scaled_data).astype(np.int16)

        print('ekgdata', ekg_data)

        print(ekg_data.shape)


        ekg_data = ekg_data.reshape((1, -1))

        # Assuming ekg_data is a NumPy array
        print(ekg_data.shape)

        # Write the data to the file
        f.writeSamples(ekg_data)

        # Close the EdfWriter
        f.close()

