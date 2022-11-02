# Kyler Olsen - August 2022

# std imports
import http.server
import configparser
import os

# local imports
from battery_data import battery_data

class ytd_HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            path = self.path[1:].split("/")
            #print(self.path,path,get_csv_files())
            if len(path) == 1 and path[0] in ["","index.html"]:
                files = battery_data.get_csv_files()
                html = battery_data.create_html_list(files).encode('utf-8')

                self.send_response(200)
                self.end_headers()
                self.wfile.write(html)
            elif len(path) == 1 and path[0] == "DefaultGraph.png":
                with open('src/DefaultGraph.png', 'rb') as img:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(img.read())
            elif len(path) == 2 and path[0] == battery_data.data_location[:-1].replace('/', '-') and path[1] in battery_data.get_csv_files():
                img = battery_data(f"{battery_data.data_location}{path[1]}.csv").get_graph()
                
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


def main():

    CONFIG_FILENAME = 'settings.config'
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'port' : 8080,
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

    if config['Battery']['enabled']:
        battery_data.data_location = config['Battery']['data location']
        if not os.path.isdir(battery_data.data_location):
            raise FileNotFoundError(f"Cannot find the path specified for tempature data: '{battery_data.data_location}'")

    # Set up and start server
    httpd = http.server.ThreadingHTTPServer(('', port),ytd_HTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
