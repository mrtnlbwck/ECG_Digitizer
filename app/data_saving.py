import csv
import mne
import pandas as pd


class DataSaving:

    def chart_to_csv(self, path, all_spline_y):

        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Generate headers based on the number of signals
            headers = [f'Signal_{i + 1}' for i in range(len(all_spline_y))]

            # Write headers
            writer.writerow(headers)

            # Transpose the data and write it to the CSV file
            for row in zip(*all_spline_y):
                writer.writerow(row)


    def csv_to_edf(self, csv_path, filename, sampling_rate):
        csv_data = pd.read_csv(csv_path)
        ch_names = list(csv_data.columns)
        data = csv_data.values

        info = mne.create_info(ch_names=ch_names, sfreq=sampling_rate, ch_types='ecg')

        raw = mne.io.RawArray(data.T, info)

        mne.export.export_raw(filename, raw, overwrite=True)