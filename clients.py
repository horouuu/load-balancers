import requests
import asyncio
import random
from time import sleep

def req_delay(port):
    sleep(3)
    res = requests.get(f"http://127.0.0.1:{port}/get")
    print(res.content)

def req(port):
    res = requests.get(f"http://127.0.0.1:{port}/get")
    print(res.content)

async def request_test():
    for port in range(5000, 5010):
        # requests will take 3 seconds longer if port is odd to test asynchronous execution
        res = asyncio.to_thread(req if port % 2 == 0 else req_delay, port)
        asyncio.create_task(res)

asyncio.run(request_test())