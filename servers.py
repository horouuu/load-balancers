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

def create_servers():
    servers = []
    global curr_port
    for i in range(NUM_SERVERS):
        appObj = MockServer.create_app(curr_port)
        t = threading.Thread(target=lambda: appObj.app().run(host='127.0.0.1', port=appObj.port(), debug=False, threaded=True))
        t.start()
        servers.append((f"127.0.0.1:{appObj.port()}"))
        curr_port += 1
        sleep(0.1)
    return servers

# if __name__ == "__main__":
#     create_servers()