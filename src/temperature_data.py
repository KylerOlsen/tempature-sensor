# Kyler Olsen Sept 2022

# std imports
import csv
import os
import io
import datetime

# installed imports
import matplotlib.pyplot as plt


class temperature_data:

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

    @classmethod
    def create_html_list(cls, data, template=(None, None)):
        """Creates an HTML file listing all the given csv files"""
        html = ""

        # Concatenate the document header and the start of the body
        if template[0] is None:
            html += "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/>\
                <style>.container{display:grid;}.left{grid-column:1;}\
                .right{grid-column:2;}</style></head>\
                <body><div class=\"container\"><h1 class=\"left\">Select a data file:</h1>\
                <ul class=\"left\">"
        else:
            html += template[0]

        # Concatenate a link to each csv file's graph
        for i in data:
            html += f"<li><a onclick=\"document.querySelector('img').src = '/{cls.data_location[:-1].replace('/', '-')}/{i}';\">{i}</a></li>"
        
        # Concatenate the end of the body and the document footer
        if template[1] is None:
            html += "</ul><img class=\"right\" src=\"DefaultGraph.png\"/></div></body></html>"
        else:
            html += template[1]
        
        # Return the HTML document
        return html

    @classmethod
    def get_csv_files(cls):
        """Returns a list of stored csv files"""

        # Get a list of all stored files
        directory_list = os.listdir(cls.data_location)

        # Filter out and store all of the csv files
        files = []
        for i in directory_list:
            if i.endswith(".csv"):
                files.append(i[:-4])
        
        # Return the list of csv files
        return files
