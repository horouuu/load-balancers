from typing import List
from flask import Flask
from flask import request
import threading
from time import sleep
from sys import maxsize
from random import choice

PORT_START = 5000
curr_port = PORT_START

class MockServer:
        class Region:
                prop_constant = 3*(10**8)
                region_map = {
                        "US-1": ("New York", 15820),
                        "SG-1": ("Singapore", 2),
                        "JP-1": ("Tokyo", 5928),
                        "EU-1": ("Berlin", 10131)
                }

                @staticmethod
                def get_latency(region: (str, int)):
                        return region[1]*1000/MockServer.Region.prop_constant

                @staticmethod
                def get_random_region():
                        map_keys = MockServer.Region.region_map.keys()
                        k = choice(map_keys)
                        return MockServer.Region.region_map[k]

                @staticmethod
                def get_region(code):
                        try:
                                return MockServer.Region.region_map[code]
                        except KeyError:
                                return ("Singapore", 2)

        def __init__(self, app, port):
                self._port = port
                self._app = app
                self._latency = 0
                self._region = MockServer.Region.get_random_region()
                self._weight = 0
                self._server_address = f"127.0.0.1:{self._port}"
                self._avg_response_time = 0
                self._total_requests = 0
                self._green = False

        @property
        def port(self):
                return self._port
        @property
        def app(self):
                return self._app

        @property
        def server_address(self):
                return self._server_address

        @property
        def latency(self):
                return self._latency

        @latency.setter
        def latency(self, dist):
                self._latency = dist

        @property
        def region(self):
                return self._region

        @region.setter
        def region(self, region):
                self._region = region

        @property
        def weight(self):
                return self._weight
        
        @weight.setter
        def weight(self, w):
                self._weight = w

        @property
        def avg_response_time(self):
                return self._avg_response_time

        @avg_response_time.setter
        def avg_response_time(self, t):
                self._avg_response_time = t

        @property
        def total_requests(self):
                return self._total_requests

        @total_requests.setter
        def total_requests(self, reqs):
                self._total_requests = reqs

        @property
        def green(self):
                return self._green

        @green.setter
        def green(self, g):
                self._green = g

        @staticmethod
        def create_app(port):       
                app = Flask(__name__)
                @app.route("/get", methods=['GET'])
                def simulate_get():
                        return f"Get request successful at port: {port}."

                @app.route("/count", methods=['GET'])
                def count_to_1000():
                        for i in range(1, 1001):
                                print(i)

                        return f"Successfully counted to 1000!"

                @app.route("/sort", methods=['POST'])
                def sort_array():
                        return None

                return MockServer(app, port)
        
"""
New class is a subclass of our MockServer but it will be considered a
"green server". That is, a server that takes into account the carbon footprint
it produces. Specifics on implementation will be given on function definition. 
"""

def create_servers(num) -> List[MockServer]:
    servers: List[MockServer] = []
    global curr_port
    for _ in range(num):
        appObj = MockServer.create_app(curr_port)
        t = threading.Thread(target=lambda: appObj.app.run(host='127.0.0.1', port=appObj.port, debug=False, threaded=True))
        t.start()
        servers.append(appObj)
        curr_port += 1
        sleep(0.1)
    return servers
