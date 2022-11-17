# Kyler Olsen Sept 2022

# std imports
import csv
# import os
import io
# import datetime
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
