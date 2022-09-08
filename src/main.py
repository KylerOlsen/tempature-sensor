# Kyler Olsen - August 2022

# std imports
import http.server
import sys

# local imports
from temperature_data import temperature_data

class ytd_HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            path = self.path[1:].split("/")
            #print(self.path,path,get_csv_files())
            if len(path) == 1 and path[0] in ["","index.html"]:
                files = temperature_data.get_csv_files()
                html = temperature_data.create_html_list(files).encode('utf-8')

                self.send_response(200)
                self.end_headers()
                self.wfile.write(html)
            elif len(path) == 2 and path[0] == 'data' and path[1] in temperature_data.get_csv_files():
                img = temperature_data(f"data/{path[1]}.csv").get_graph()
                
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

    # Get port from command line arguments or set default
    if ('-p' in sys.argv and
        len(sys.argv) > sys.argv.index('-p') + 1 and
        sys.argv[sys.argv.index('-p') + 1].isdecimal()):
            port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        port = 8080

    # Set up and start server
    httpd = http.server.ThreadingHTTPServer(('', port),ytd_HTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
