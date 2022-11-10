# Kyler Olsen Sept 2022

# std imports
import os
from abc import ABC, abstractmethod
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Data(ABC):

    data_location = 'data/'

    @abstractmethod
    def __init__(self,filename):
        """Loads data from a csv file."""
        self.filename = filename
    
    @abstractmethod
    def __dict__(self): pass

    @abstractmethod
    def get_graph(self):
        """Returns the graph for the data set as an image in a file-like object"""

    @abstractmethod
    def get_json(self):
        """Returns the data set in json format"""

    # @classmethod
    # def create_html_list(cls, data, template=(None, None)):
    #     """Creates an HTML file listing all the given csv files"""
    #     html = ""

    #     # Concatenate the document header and the start of the body
    #     if template[0] is None:
    #         html += "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/>\
    #             <style>.container{display:grid;}.left{grid-column:1;}\
    #             .right{grid-column:2;}</style></head>\
    #             <body><div class=\"container\"><h1 class=\"left\">Select a data file:</h1>\
    #             <ul class=\"left\">"
    #     else:
    #         html += template[0]

    #     # Concatenate a link to each csv file's graph
    #     for i in data:
    #         html += f"<li><a onclick=\"document.querySelector('img').src = '/?graph={cls.data_location[:-1].replace('/', '-')}/{i}';\">{i}</a></li>"
        
    #     # Concatenate the end of the body and the document footer
    #     if template[1] is None:
    #         html += "</ul><img class=\"right\" src=\"/?graph=DefaultGraph.png\"/></div></body></html>"
    #     else:
    #         html += template[1]
        
    #     # Return the HTML document
    #     return html

    @classmethod
    def get_csv_files(cls):
        """Returns a list of stored csv files"""

        # Filter out and store all of the csv files
        all_files = []
        for root, folders, files in os.walk(cls.data_location):
            for i in files:
                if i.endswith(".csv"):
                    all_files.append(root[len(cls.data_location):].replace('\\','/') + '/' + i[:-4])
        
        # Return the list of csv files
        return all_files

    @classmethod
    def get_csv_filetree(cls):
        """Returns a list of stored csv files"""

        # Filter out and store all of the csv files
        file_tree = {"folders":{},"files":[]}
        for root, folders, files in os.walk(cls.data_location):
            current_tree = file_tree
            for i in root[len(cls.data_location):].replace('\\','/').split('/'):
                if i != '': current_tree = current_tree['folders'][i]
            for i in folders:
                current_tree['folders'][i] = {"folders":{},"files":[]}
            for i in files:
                if i.endswith(".csv"):
                    current_tree['files'].append(i[:-4])
        
        # Return the list of csv files
        return file_tree

    @classmethod
    def http(cls, request):
        files = cls.get_csv_files()
        url = urlparse(request.path)
        path = url.path[1:].split("/")[1:]
        query = parse_qs(url.query)
        print(url,path,query)
        if (len(path) == 1 and path[0].lower() in ["files","files.json"]) or (len(path) == 0 and 'files' in query and query['files'][0].lower() == "true"):
            data = json.dumps(cls.get_csv_filetree())
            
            request.send_response(200)
            request.end_headers()
            request.wfile.write(data.encode('utf-8'))
        elif len(path) == 0 and 'data' in query and query['data'][0] in files:
            data = cls(f"{cls.data_location}/{query['data'][0]}.csv").get_json()
            
            request.send_response(200)
            request.end_headers()
            request.wfile.write(data.encode('utf-8'))
        else:
            request.send_response(404)
            request.end_headers()
            
