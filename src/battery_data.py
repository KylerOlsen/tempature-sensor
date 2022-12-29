# Kyler Olsen Sept 2022

# std imports
import csv
# import os
import io
import datetime
import json

# installed imports
import matplotlib.pyplot as plt

# local imports
from data import Data


class battery_data(Data):

    data_location = 'data/battery/'

    def __init__(self,filename):
        """Loads data from a csv file."""

        # Opens the file and initilazes varables to load data into
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.filename = filename
            self.data = {}
            self._voltage = []

            # Loads in the data, one line at a time
            for line in csv_reader:
                if len(line) == 2:
                    self.data[line[0]] = line[1]
                elif len(line) == 1 and line[0] == "Voltage":
                    break

            for line in csv_reader:
                self._voltage.append(float(line[0]))

    def __dict__(self):
        return self.data

    def get_graph(self):
        """Returns the graph for the data set as an image in a file-like object"""

        # Generates a plot for the file
        fig, ax = plt.subplots()
        ax.plot(range(950, 1350), self._voltage[950:1350], linewidth=2.0)
        # Add and format Labels
        ax.set_title(f"{self.filename.split('/')[-1]}: Voltage over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Voltage")
        ax.grid(True)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=20, horizontalalignment='right')

        # Saves the figure (graph) as a png into a file like object
        img = io.BytesIO()
        plt.savefig(img,format='png',bbox_inches='tight')
        img.seek(0)
        return img

    def get_json(self):
        times = {
            "Total Elapsed Time(s)" : "Total Elapsed Time",
            "Elapsed Time(s)" : "Elapsed Time",
            "Running Time(s)" : "Running Time",
            "Not Running Time(s)" : "Not Running Time",
            "Cranking Time(s)" : "Cranking Time",
        }
        data = {"Filename" : self.filename[len(self.data_location):]}
        for key, value in self.data.items():
            if key in times:
                v = int(float(value))
                hours = v // 3600
                minutes = (v // 60) % 60
                seconds = v % 60
                data[times[key]] = f"{hours}:{minutes:02}:{seconds:02}.{int(round((float(value)-v) * 100)):02} ({value}s)"
            elif key == "Temperature":
                data[key] = f"{(float(value) * 9 / 5) + 32:.1f}°F ({value}°C)"
            else:
                data[key] = value
        return json.dumps({"metadata" : data, "data" : self._voltage[950:1350]})

    @staticmethod
    def is_valid_name(name: str):
        return name.endswith(".csv") and name.startswith("4")


class battery_event_data(battery_data):

    def __init__(self,filename):
        """Loads data from a csv file."""

        # Opens the file and initilazes varables to load data into
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.filename = filename
            self._datetime = []
            self._total_elapsed = []
            self._elapsed = []
            self._event = []
            self._vmax = []
            self._vave = []
            self._vmin = []
            self._tmax = []
            self._tave = []
            self._tmin = []

            # Loads in the data, one line at a time
            for line in csv_reader:
                # Line date and time
                self._datetime.append(datetime.datetime.fromisoformat(line[0]))
                # Line total elapsed time
                self._total_elapsed.append(float(line[1]))
                # Line elapsed time
                self._elapsed.append(float(line[2]))
                # Line event name
                self._event.append(line[3])
                # Line vmax
                self._vmax.append(float(line[4]))
                # Line vave
                self._vave.append(float(line[5]))
                # Line vmin
                self._vmin.append(float(line[6]))
                # Line tmax
                self._tmax.append(float(line[7]))
                # Line tave
                self._tave.append(float(line[8]))
                # Line tmin
                self._tmin.append(float(line[9]))

    def __dict__(self):
        return self.data

    def get_json(self):
        date_time = []
        for i in range(len(self._datetime)):
            date_time.append(self._datetime[i].isoformat())
        total_elapsed = []
        for i in range(len(self._total_elapsed)):
            v = int(float(self._total_elapsed[i]))
            hours = v // 3600
            minutes = (v // 60) % 60
            seconds = v % 60
            total_elapsed.append(f"{hours}:{minutes:02}:{seconds:02}.{int(round((float(self._total_elapsed[i])-v) * 100)):02} ({self._total_elapsed[i]}s)")
        elapsed = []
        for i in range(len(self._elapsed)):
            v = int(float(self._elapsed[i]))
            hours = v // 3600
            minutes = (v // 60) % 60
            seconds = v % 60
            elapsed.append(f"{hours}:{minutes:02}:{seconds:02}.{int(round((float(self._elapsed[i])-v) * 100)):02} ({self._elapsed[i]}s)")
        data = {
            "datetime" : date_time,
            "total_elapsed" : total_elapsed,
            "elapsed" : elapsed,
            "event" : self._event,
            "vmax" : self._vmax,
            "vave" : self._vave,
            "vmin" : self._vmin,
            "tmax" : self._tmax,
            "tave" : self._tave,
            "tmin" : self._tmin,
        }
        return json.dumps({"metadata" : {"Filename" : self.filename[len(self.data_location):]}, "data" : data})
