import asyncio
from typing import List, Dict
from load_balancer import LoadBalancer
from servers import MockServer, create_servers
from time import time
from sys import argv

NUM_CLIENTS = 10
NUM_REQUESTS = 10   # Note :: This will be PER CLIENT. if NUM_CLIENTS = 10 and NUM_REQUEST = 100; then
                    # total number of requests is 1000

# Dict allows us to allocate which server regions we would like to use and how many of those should be green.
SEVER_PARAMS: Dict[str, int] = {
    "US-1 Normal"       : 1,
    "US-1 Green"        : 0,

    "SG-1 Normal"       : 2,
    "SG-1 Green"        : 1,
    
    "JP-1 Normal"       : 1,
    "JP-1 Green"        : 3,
    
    "EU-1 Normal"       : 1,
    "EU-1 Green"        : 0,
}

def main():
    asyncio.run(static_lb_simulation()) # Weighted Round Robin (Static) Load Balancer Algorithm

async def static_lb_simulation(): 

    if "-dynamic" in argv:
        isDynamic = True
    else: 
        isDynamic = False

    servers: List[MockServer] = create_servers(SEVER_PARAMS, isDynamic)
    t = time()
    await LoadBalancer.simulate_weighted_round_robin(servers, NUM_CLIENTS, NUM_REQUESTS, isDynamic)
    t = time() - t

    print("-------------------")
    print(f"Summary {'(Dynamic)' if isDynamic else ''}")
    print("-------------------")
    print(f"Time taken: {t*1000} ms to complete {NUM_REQUESTS * NUM_CLIENTS} requests.\n")
    for server in sorted(servers, key= lambda s: s.weight, reverse=True):
        print(f"{server.region[0]}{" (Green)" if server.green else ""}:\nAverage response time: {server.avg_response_time} ms\nWeight: {server.weight}\nTotal # of requests: {server._total_requests}\n")

if __name__ == "__main__": 
    main()