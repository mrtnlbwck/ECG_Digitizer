import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


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

        # Tworzenie obiektu DataFrame z danymi
        df = pd.DataFrame(data)

        # Obliczenie średniej wartości y dla każdej unikalnej wartości x
        average_y = df.groupby('x')['y'].mean().reset_index()

        new_y = np.array(average_y['y'])
        new_x = np.array(average_y['x'])

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

        plt.plot(x_interp, y_linear(x_interp), "red")
        plt.title('Wykres EKG')
        plt.show()

