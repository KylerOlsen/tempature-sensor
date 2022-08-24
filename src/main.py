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


def load_tempature_data(filename):
    """Loads data from a csv file and returns the data for a graph"""

    """
    Field indexes
        datetime : 0
        index : 1
        tempature : 2
        bat-voltage : 3
        wireless-strength : 4
    """

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        time_data = []
        tempature_data = []
        voltage_data = None
        wireless_strength = []
        for line in csv_reader:
            time_data.append(datetime.datetime.fromisoformat(line[0]))
            tempature_data.append(float(line[2]))
            if voltage_data is None: voltage_data = float(line[3])
            else: voltage_data = min(voltage_data,float(line[3]))
            wireless_strength.append(int(line[4]))
    
        return {'datetime':time_data, 'tempature':tempature_data, 'min_bat_volts':voltage_data, 'wireless_strength':wireless_strength}

def get_tempature_graph(filename):
    data = load_tempature_data(filename)

    wifi_avg = sum(data['wireless_strength'])//len(data['wireless_strength'])
    wifi_min = min(data['wireless_strength'])
    wifi_max = max(data['wireless_strength'])

    print(f"Battery Level : {data['min_bat_volts']}, Wifi Strength : max {wifi_max} dBm, min {wifi_min} dBm, avg {wifi_avg} dBm")

    fig, ax = plt.subplots()
    ax.plot(data['datetime'], data['tempature'], linewidth=2.0)
    ax.set_xlabel('Time')
    ax.set_ylabel('Tempature')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')
    plt.show()

def main():
    get_tempature_graph("data/3000-Data.csv")

if __name__ == "__main__":
    main()
