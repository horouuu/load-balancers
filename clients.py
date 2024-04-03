from typing import List
import requests
import asyncio
from servers import MockServer

async def req_delay(server: MockServer):
    await asyncio.sleep(3)
    res = requests.get(f"http://{server.server_address}/get")
    print(bytes.decode(res.content, res.encoding))

async def req(server: MockServer):
    res = requests.get(f"http://{server.server_address}/get")
    print(bytes.decode(res.content, res.encoding))

async def request_test():
    for port in range(5000, 5010):
        # requests will take 3 seconds longer if port is odd to test asynchronous execution
        res = asyncio.to_thread(req if port % 2 == 0 else req_delay, port)
        asyncio.create_task(res)

async def request_test(balancer):
    for _ in range(10):
        server = balancer.get_next_server()
        serverInstance = server.get_instance()
        print("server: ", server.get_instance())
        asyncio.create_task(req(serverInstance))