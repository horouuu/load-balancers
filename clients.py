from typing import List
import requests
from servers import MockServer
from time import time, sleep

NUM_SERVERS = 10

def req(server: MockServer):
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