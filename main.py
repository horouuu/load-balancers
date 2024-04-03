import asyncio
from typing import List
from load_balancer import LoadBalancer
from servers import MockServer, create_servers
from weighted_round_robin import WeightedRoundRobin
from time import time

def main():
    static_lb_simulation() # Weighted Round Robin (Static) Load Balancer Algorithm

def static_lb_simulation(): 
    servers: List[MockServer] = create_servers()
    weighted_servers: dict[MockServer, int] = WeightedRoundRobin.assign_weights(servers)
    t = time()
    asyncio.run(LoadBalancer.simulate_weighted_round_robin(weighted_servers, 500))
    t = time() - t
    print(f"Time taken: {t*1000} ms")

if __name__ == "__main__": 
    main()