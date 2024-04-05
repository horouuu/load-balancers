from typing import List
from flask import Flask
import threading
from time import sleep

NUM_SERVERS = 10
PORT_START = 5000
curr_port = PORT_START

class MockServer:
        def __init__(self, app, port):
                self._port = port
                self._app = app
                self.weight = 0
                self.server_address = f"127.0.0.1:{self._port}"

        def port(self):
                return self._port

        def app(self):
                return self._app

        @staticmethod
        def create_app(port):       
                app = Flask(__name__)
                @app.route("/get")
                def simulate_get():
                        return f"Get request successful at port: {port}."

                return MockServer(app, port)
        
"""
New class is a subclass of our MockServer but it will be considered a
"green server". That is, a server that takes into account the carbon footprint
it produces. Specifics on implementation will be given on function definition. 
"""

class GreenServer(MockServer):
        def __init__(self, app, port, mu_footprint: int):
              super().__init__(app, port)
              self._mean_carbon_footprint = mu_footprint
        
        def port(self):
               return super().port()
       
        def app(self):
              return super().app()

        # For now this will be the rudimentary "implementation"
        # of our green's server carbon emmision. Server has some average
        # carbon emission. But it is normally randomized as time passes.
        def get_carbon_emission(self):
               from numpy import random
               from math import sqrt
               return random.normal(loc=self._mean_carbon_footprint,
                                    scale=sqrt(self._mean_carbon_footprint))

        @staticmethod
        def create_app(port):
                app = Flask(__name__)
                @app.route("/get")
                def simulate_get():
                       return f"get"
       


def create_servers() -> List[MockServer]:
    servers: List[MockServer] = []
    global curr_port
    for _ in range(NUM_SERVERS):
        appObj = MockServer.create_app(curr_port)
        t = threading.Thread(target=lambda: appObj.app().run(host='127.0.0.1', port=appObj.port(), debug=False, threaded=True))
        t.start()
        servers.append(appObj)
        curr_port += 1
        sleep(0.1)
    return servers
