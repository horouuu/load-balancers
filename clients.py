import requests
import asyncio
import random
from time import sleep
from servers import create_servers
# LBAs
from load_balancers.weighted_round_robin import WeightedRoundRobin

async def req_delay(server):
    await asyncio.sleep(3)
    res = requests.get(f"http://{server}/get")
    print(res.content)

async def req(server):
    res = requests.get(f"http://{server}/get")
    print(res.content)

# async def request_test():
#     for port in range(5000, 5010):
#         # requests will take 3 seconds longer if port is odd to test asynchronous execution
#         res = asyncio.to_thread(req if port % 2 == 0 else req_delay, port)
#         asyncio.create_task(res)

async def request_test(balancer):
    for _ in range(10):
        server = balancer.get_next_server()
        serverInstance = server.get_instance()
        print("server: ", server.get_instance())
        asyncio.create_task(req(serverInstance))

if __name__ == "__main__":
    servers = create_servers()  # Get the list of servers from servers.py
    weightedServerList = []
    a = 1
    for i in servers:
        weightedServerList.append(WeightedRoundRobin.Server(i, a))
        print(i, a)
        a += 1
    balancer = WeightedRoundRobin(weightedServerList)
    asyncio.run(request_test(balancer))