import asyncio
from typing import List
from load_balancer import LoadBalancer
from servers import MockServer, create_servers
from load_balancers.weighted_round_robin import WeightedRoundRobin
from time import time

NUM_SERVERS = 10
NUM_REQUESTS = 10000

def main():
    static_lb_simulation() # Weighted Round Robin (Static) Load Balancer Algorithm

def static_lb_simulation(): 
    servers: List[MockServer] = create_servers(NUM_SERVERS)
    weighted_servers: dict[MockServer, int] = WeightedRoundRobin.assign_weights(servers)
    t = time()
    asyncio.run(LoadBalancer.simulate_weighted_round_robin(weighted_servers, NUM_REQUESTS))
    t = time() - t
    print(f"Time taken: {t*1000} ms to complete {NUM_REQUESTS} requests.")
    for server in servers:
        print(server.avg_response_time, server.weight)

if __name__ == "__main__": 
    main()