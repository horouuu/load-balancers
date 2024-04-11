import requests
from servers import MockServer
from time import time, sleep

# We assume all clients reside in Singapore!
class MockClient:
    def __init__(self) -> None:
        # If true, request should have some tag to let LB know client needs a fast response time.
        self._fast_response = False
    @property
    def fast_response(self):
        return self._fast_response
    
    @fast_response.setter
    def fast_response(self, state: bool):
        self._fast_response = state

    # Generate n requests.
    def req(self, server: MockServer, num_of_requests: int = 1):
        for _ in range(num_of_requests):
            t = time()
            res = requests.get(f"http://{server.server_address}/get")
            sleep(server.latency/1000)
            t = time() - t
            server.avg_response_time = server.avg_response_time * server.total_requests
            server.total_requests += 1
            server.avg_response_time = (server.avg_response_time + t*1000)/server.total_requests
            print(bytes.decode(res.content, res.encoding))
            print(f"Region: {server.region}")
            print(f"Latency: {server.latency}")
