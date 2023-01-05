# Kyler Olsen - August 2022

# std imports
import http.server
import configparser
import os
import os.path
from urllib.parse import parse_qs, urlparse

# local imports
from temperature_data import temperature_data
from battery_data import battery_data, battery_event_data

class ytd_HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print()
        try:
            path = urlparse(self.path).path[1:].split("/")
            if len(path) == 1 and path[0].lower() in ["",]:
                with open("src/index.html",'rb') as data:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(data.read())
            elif len(path) == 1 and path[0].lower() in ["index.html","index.css","index.js","defaultgraph.png"]:
                with open("src/"+path[0].lower(),'rb') as data:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(data.read())
            elif len(path) >= 1 and path[0].lower() in ["battery","battery.php"]:
                url = urlparse(self.path)
                query = parse_qs(url.query)
                if 'data' in query and query['data'][0].endswith("EventData"):
                    battery_event_data.http(self)
                else:
                    battery_data.http(self)
            elif len(path) >= 1 and path[0].lower() in ["temperature","temperature.php"]:
                temperature_data.http(self)
            elif len(path) >= 1 and path[0].lower() == "--exit--" and self.client_address[0] == '127.0.0.1':
                self.send_response(200)
                self.end_headers()
                self.server.shutdown()
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


def main():

    CONFIG_FILENAME = 'settings.config'
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'port' : 8080,
    }
    config['Temperature'] = {
        'enabled' : False,
        'data location' : 'data/temperature/',
    }
    config['Battery'] = {
        'enabled' : False,
        'data location' : 'data/battery/',
    }

    if os.path.isfile(CONFIG_FILENAME):
        #with open(CONFIG_FILENAME) as configfile:
        config.read(CONFIG_FILENAME)
    with open(CONFIG_FILENAME, 'w') as configfile:
        config.write(configfile)

    port = int(config['DEFAULT']['port'])

    if config['Temperature']['enabled']:
        temperature_data.data_location = os.path.expanduser(config['Battery']['data location'])
        if not os.path.isdir(temperature_data.data_location):
            raise FileNotFoundError(f"Cannot find the path specified for tempature data: '{temperature_data.data_location}'")

    if config['Battery']['enabled']:
        battery_data.data_location = os.path.expanduser(config['Battery']['data location'])
        if not os.path.isdir(battery_data.data_location):
            raise FileNotFoundError(f"Cannot find the path specified for tempature data: '{battery_data.data_location}'")

    # Set up and start server
    httpd = http.server.ThreadingHTTPServer(('', port),ytd_HTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    # battery_data.data_location = 'data/'
    # print(battery_data.get_csv_files())
    main()
