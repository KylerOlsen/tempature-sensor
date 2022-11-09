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
        data = {"Filename" : self.filename}
        for key, value in self.data.items():
            data[key] = value
        return json.dumps({"metadata" : data, "data" : self._voltage[950:1350]})
