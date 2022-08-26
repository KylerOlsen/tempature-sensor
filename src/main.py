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
        try:
            path = self.path[1:].split("/")
            #print(self.path,path,get_csv_files())
            if len(path) == 1 and path[0] in ["","index.html"]:
                files = get_csv_files()
                html = create_html_list(files).encode('utf-8')

                self.send_response(200)
                self.end_headers()
                self.wfile.write(html)
            elif len(path) == 2 and path[0] == 'data' and path[1] in get_csv_files():
                img = tempature_data(f"data/{path[1]}.csv").get_graph()
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(img.read())
            else:
                self.send_response(404)
                self.end_headers()
        except Exception:
            self.send_response(500)
            self.end_headers()
            raise

    def do_POST(self):
        try:
            path = self.path[1:].split("/")
            self.send_response(405)
            self.end_headers()
        except Exception:
            self.send_response(500)
            self.end_headers()
            raise


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

        # Generates a plot for the file
        fig, ax = plt.subplots()
        ax.plot(self._datetime, self._tempature, linewidth=2.0)
        # Add and format Labels
        ax.set_title('Tempature over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('Tempature')
        ax.grid(True)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=20, horizontalalignment='right')
        
        # Saves the figure (graph) as a png into a file like object
        img = io.BytesIO()
        plt.savefig(img,format='png',bbox_inches='tight')
        img.seek(0)
        return img


def create_html_list(data, template=(None, None)):
    """Creates an HTML file listing all the given csv files"""
    html = ""

    # Concatenate the document header and the start of the body
    if template[0] is None:
        html += "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/></head><body>"
    else:
        html += template[0]

    # Concatenate a link to each csv file's graph
    for i in data:
        html += f"<a href=\"/data/{i}\">{i}</a><br>"
    
    # Concatenate the end of the body and the document footer
    if template[1] is None:
        html += "</body></html>"
    else:
        html += template[1]
    
    # Return the HTML document
    return html

def get_csv_files(directory="data/"):
    """Returns a list of stored csv files"""

    # Get a list of all stored files
    directory_list = os.listdir(directory)

    # Filter out and store all of the csv files
    files = []
    for i in directory_list:
        if i.endswith(".csv"):
            files.append(i.removesuffix(".csv"))
    
    # Return the list of csv files
    return files

def main():
    # Set up and start server
    httpd = http.server.ThreadingHTTPServer(('', 8080),ytd_HTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
