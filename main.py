import asyncio
from typing import List, Dict
from load_balancer import LoadBalancer
from servers import MockServer, create_servers
from load_balancers.weighted_round_robin import WeightedRoundRobin
from time import time

NUM_CLIENTS = 1
NUM_REQUESTS = 1000    # Note :: This will be PER CLIENT. if NUM_CLIENTS = 10 and NUM_REQUEST = 100; then
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
    servers: List[MockServer] = create_servers(SEVER_PARAMS)
    weighted_servers: dict[MockServer, int] = WeightedRoundRobin.assign_weights(servers)
    t = time()
    await LoadBalancer.simulate_weighted_round_robin(weighted_servers, NUM_CLIENTS, NUM_REQUESTS)
    t = time() - t
    total_power_usage = 0
    total_green = 0
    total_requests = 0
    print(f"Time taken: {t*1000} ms to complete {NUM_REQUESTS} requests.")
    for server in servers:
        if server.green: total_green += 1
        total_requests += server.total_requests
        total_power_usage += server.trans_power_usage
        print(server.avg_response_time, server.weight, server.total_requests, server.region)

    print(f"Total requests served: {total_requests}")
    print(f"Total power used in transmitting data: {total_power_usage/1000} kW.")
    print(f"Total green requests: {total_green}")
    print(f"Percentage of requests that used green energy servers: {total_green/total_requests * 100}%")

if __name__ == "__main__": 
    main()