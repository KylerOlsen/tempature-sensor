# Kyler Olsen - August 2022

# std imports
import http.server
import csv
import os
import io
import datetime

# installed imports
import matplotlib.pyplot as plt

class ytd_HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        pass

    def do_POST(self):
        pass


class tempature_data:

    def __init__(self,filename):
        """Loads data from a csv file."""

        """
        Field indexes
            datetime : 0
            index : 1
            tempature : 2
            bat-voltage : 3
            wireless-strength : 4
        """

        # Opens the file and initilazes varables to load data into
        with open(filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self._datetime = []
            self._tempature = []
            self._bat_volts = []
            self._wireless_strength = []

            # Loads in the data, one line at a time
            for line in csv_reader:
                # Line date and time
                self._datetime.append(datetime.datetime.fromisoformat(line[0]))
                # Line tempature
                self._tempature.append(float(line[2]))
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
        fig, ax = plt.subplots()
        ax.plot(self._datetime, self._tempature, linewidth=2.0)
        ax.set_title('Tempature over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Tempature')
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=25, horizontalalignment='right')
        
        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        return img


def main():
    img = tempature_data("data/3000-Data.csv").get_graph()
    with open("data/3000-Data.png", 'wb') as img_file:
        img_file.write(img.read())

if __name__ == "__main__":
    main()
