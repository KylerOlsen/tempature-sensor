# Kyler Olsen Sept 2022

# std imports
import csv
import io
import datetime
import json

# installed imports
import matplotlib.pyplot as plt

# local imports
from data import Data


class acceleration_data(Data):

    data_location = 'data/acceleration/'

    def __init__(self,filename):
        """Loads data from a csv file."""

        """
        Field indexes
            datetime : 0
            index : 1
            temperature : 2
            bat-voltage : 3
            wireless-strength : 4
        """

        # Opens the file and initilazes varables to load data into
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.filename = filename
            self.data_filename = filename.replace('D', 'S')
            self._x = []
            self._y = []
            self._z = []

            # Loads in the data, one line at a time
            for line in csv_reader:
                if csv_reader.line_num > 1:
                    self._x.append(float(line[0]))
                    self._y.append(float(line[1]))
                    self._z.append(float(line[2]))

            # Open the data file and load the data from it
            with open(self.data_filename, 'r') as data_file:
                self._ver = "Unknown"
                self._temp = 0.0
                self._batt_volt = 0.0
                self._wifi = 0.0
                self._files_sent = 0
                self._x_ave = 0.0
                self._y_ave = 0.0
                self._z_ave = 0.0
                self._abs_x_max = 0.0
                self._abs_y_max = 0.0
                self._abs_z_max = 0.0
                self._rms_x = 0.0
                self._rms_y = 0.0
                self._rms_z = 0.0
                for line in data_file:
                    if line.startswith("Version"):
                        self._ver = line.rsplit(':')[-1]
                    if line.startswith("Temperature(C)"):
                        self._temp = float(line.rsplit(',')[-1])
                    if line.startswith("Battery(V)"):
                        self._batt_volt = float(line.rsplit(',')[-1])
                    if line.startswith("WiFi Strenght(dB)"):
                        self._wifi = float(line.rsplit(',')[-1])
                    if line.startswith("Files Sent"):
                        self._files_sent = int(line.rsplit(',')[-1])
                    if line.startswith("X Ave (mg)"):
                        self._x_ave = float(line.rsplit(',')[-1])
                    if line.startswith("Y Ave (mg)"):
                        self._y_ave = float(line.rsplit(',')[-1])
                    if line.startswith("Z Ave (mg)"):
                        self._z_ave = float(line.rsplit(',')[-1])
                    if line.startswith("|X| Max (mg)"):
                        self._abs_x_max = float(line.rsplit(',')[-1])
                    if line.startswith("|Y| Max (mg)"):
                        self._abs_y_max = float(line.rsplit(',')[-1])
                    if line.startswith("|Z| Max (mg)"):
                        self._abs_z_max = float(line.rsplit(',')[-1])
                    if line.startswith("RMS X(mg)"):
                        self._rms_x = float(line.rsplit(',')[-1])
                    if line.startswith("RMS Y(mg)"):
                        self._rms_y = float(line.rsplit(',')[-1])
                    if line.startswith("RMS Z(mg)"):
                        self._rms_z = float(line.rsplit(',')[-1])

    def __dict__(self):
        return {
            "Version" : self._ver,
            "Temperature(C)" : self._temp,
            "Battery(V)" : self._batt_volt,
            "WiFi Strenght(dB)" : self._wifi,
            "Files Sent" : self._files_sent,
            "X Ave (mg)" : self._x_ave,
            "Y Ave (mg)" : self._y_ave,
            "Z Ave (mg)" : self._z_ave,
            "|X| Max (mg)" : self._abs_x_max,
            "|Y| Max (mg)" : self._abs_y_max,
            "|Z| Max (mg)" : self._abs_z_max,
            "RMS X(mg)" : self._rms_x,
            "RMS Y(mg)" : self._rms_y,
            "RMS Z(mg)" : self._rms_z,
        }

    def get_graph(self):
        """Returns the graph for the data set as an image in a file-like object"""

    def get_json(self):
        data = {
            "Filename" : self.filename[len(self.data_location):],
            "Data Filename" : self.data_filename[len(self.data_location):],
            "Version" : self._ver,
            "Temperature" : f"{(float(self._temp) * 9 / 5) + 32:.1f}°F ({self._temp}°C)",
            "Battery(V)" : self._batt_volt,
            "WiFi Strenght(dB)" : self._wifi,
            "Files Sent" : self._files_sent,
            "X Ave (mg)" : self._x_ave,
            "Y Ave (mg)" : self._y_ave,
            "Z Ave (mg)" : self._z_ave,
            "|X| Max (mg)" : self._abs_x_max,
            "|Y| Max (mg)" : self._abs_y_max,
            "|Z| Max (mg)" : self._abs_z_max,
            "RMS X(mg)" : self._rms_x,
            "RMS Y(mg)" : self._rms_y,
            "RMS Z(mg)" : self._rms_z,
        }
        return json.dumps({"metadata" : data, "x_data" : self._x, "y_data" : self._y, "z_data" : self._z,})

    @staticmethod
    def is_valid_name(name: str):
        return name.endswith(".csv") and name.startswith("1") and 'D' in name
