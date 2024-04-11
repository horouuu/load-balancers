from cmath import exp
from typing import List, Dict, Tuple
from flask import Flask
import threading
from time import sleep, time
from random import choice

PORT_START = 5000
curr_port = PORT_START

class MockServer:
        class Region:
                processing_delay = True
                prop_constant = 2.1*(10**8)
                region_map = {
                        "US-1": ("New York", 15330),
                        "SG-1": ("Singapore", 2),
                        "JP-1": ("Tokyo", 5320),
                        "EU-1": ("Berlin", 10000)
                }

                @staticmethod
                def get_latency(region: Tuple[str, int]): # returns RTT latency in ms
                        cls_delay = 40 * 2 # CLS to local server RTT
                        if (region[0] == "Singapore"):
                                cls_delay = 0 # CLS not used in local transmissions

                        return 2*(region[1]*1000/MockServer.Region.prop_constant*1000 + 8*MockServer.Region.processing_delay) + cls_delay

                @staticmethod
                def get_random_region():
                        map_keys = list(MockServer.Region.region_map.keys())
                        k = choice(map_keys)
                        return MockServer.Region.region_map[k]

                @staticmethod
                def get_region(code):
                        try:
                                return MockServer.Region.region_map[code]
                        except KeyError:
                                return ("Singapore", 2)

        def __init__(self, port, capacity=10):
                self._port = port
                self._app = None
                self._region = MockServer.Region.get_random_region()
                self._weight = 0
                self._server_address = f"127.0.0.1:{self._port}"
                self._avg_response_time = 0
                self._total_requests = 0
                self._green = False
                self._capacity = capacity

                # TODO: Research how much CO2/Req is released
                self._carbon_emission = None
                # TODO: Research Server's energy consumption.
                self._energy_usage = None

                # variables for fake congestion
                self.time_of_first_request_in_span = time()
                self.window = 1 # window of time that the server considers
                self.num_of_req_in_window = 0

                self._latency = MockServer.Region.get_latency(self.region)

        @property
        def port(self):
                return self._port

        @property
        def app(self):
                return self._app
        
        @app.setter
        def app(self, app):
                self._app = app


        @property
        def server_address(self):
                return self._server_address

        @property
        def latency(self):
                return self._latency

        @property
        def region(self):
                return self._region

        @region.setter
        def region(self, region):
                self._region = region
                self._latency = MockServer.Region.get_latency(region)

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
        def terminate_app(self, app: Flask):
                pass

        def update_weight(self):
                # Percentage of server 
                server_load = self.num_of_req_in_window / self._capacity

                if server_load < .50:
                        self.weight += .125
                else:
                        self.weight -= .125
    

        def create_app(self, isDynamic: bool = False) -> Flask:       
                app = Flask(__name__)
                @app.route("/get", methods=['GET'])
                def simulate_get():
                        if time() > self.time_of_first_request_in_span + self.window:
                                self.time_of_first_request_in_span = time()
                                self.num_of_req_in_window = 1
                        else:
                                # Adjust multiplicative factor to increase amount of delay
                                sleep(exp(self.num_of_req_in_window/1000*10*10))
                                self.num_of_req_in_window += 1
                        
                        if isDynamic:
                                self.update_weight()
                        return f"Get request successful at port: {self.port}."

                self.app = app
                return app

# Server Params allows us to specify region and whether a server is green.
def create_servers(server_params: Dict[str, int], isDynamic=False) -> List[MockServer]:
    servers: List[MockServer] = []
    global curr_port
    for server_type, server_num in server_params.items():
        server_info = server_type.split(' ')
        for _ in range(server_num):
            server = MockServer(curr_port)
            server_app = server.create_app(isDynamic)
            server.region = MockServer.Region.get_region(server_info[0])
            server.green  = (True if server_info[1] == "Green" else False)
            
            # Start server threat
            t = threading.Thread(target= lambda: server_app.run(host='127.0.0.1', port=server.port, debug=False, threaded=True))
            t.start()
            servers.append(server)
            curr_port += 1
            sleep(0.1)

    return servers
