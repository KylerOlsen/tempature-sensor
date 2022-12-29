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


class temperature_data(Data):

    data_location = 'data/temperature/'

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
            self._datetime = []
            self._temperature = []
            self._bat_volts = []
            self._wireless_strength = []

            # Loads in the data, one line at a time
            for line in csv_reader:
                # Line date and time
                self._datetime.append(datetime.datetime.fromisoformat(line[0]))
                # Line temperature
                self._temperature.append(float(line[2]))
                # Line battery voltage
                self._bat_volts.append(float(line[3]))
                # Line wireless strength
                self._wireless_strength.append(int(line[4]))

            # Calculate Battey and Wifi strength statistics
            self._bat_volts_min = min(self._bat_volts)
            self._wifi_avg = sum(self._wireless_strength)//len(self._wireless_strength)
            self._wifi_min = min(self._wireless_strength)
            self._wifi_max = max(self._wireless_strength)

    def __dict__(self):
        return {
            "bat_volts_min":self._bat_volts_min,
            "wifi_avg":self._wifi_avg,
            "wifi_min":self._wifi_min,
            "wifi_max":self._wifi_max,
        }

    def get_graph(self):
        """Returns the graph for the data set as an image in a file-like object"""

        # Generates a plot for the file
        fig, ax = plt.subplots()
        ax.plot(self._datetime, self._temperature, linewidth=2.0)
        # Add and format Labels
        ax.set_title(f"{self.filename.split('/')[-1]}: temperature over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("temperature")
        ax.grid(True)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=20, horizontalalignment='right')

        # Saves the figure (graph) as a png into a file like object
        img = io.BytesIO()
        plt.savefig(img,format='png',bbox_inches='tight')
        img.seek(0)
        return img

    def get_json(self):
        data = {
            "Filename" : self.filename[len(self.data_location):],
            "Battery volts min" : self._bat_volts_min,
            "WIFI max" : self._wifi_max,
            "WIFI avg" : self._wifi_avg,
            "WIFI min" : self._wifi_min,
        }
        temperature = []
        for value in self._temperature:
            temperature.append((float(value) * 9 / 5) + 32)
        return json.dumps({"metadata" : data, "data" : temperature})

    @staticmethod
    def is_valid_name(name: str):
        return name.endswith(".csv") and name.startswith("3")
