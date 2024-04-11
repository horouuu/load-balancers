import collections
import threading
from typing import List, Dict
from clients import MockClient
from servers import MockServer
from load_balancers.weighted_round_robin_prob import WeightedRoundRobin
from time import sleep

class LoadBalancer: 
    def __init__(self):
        pass

    async def simulate_weighted_round_robin(servers: List[MockServer], num_of_clients: int, num_of_requests: int):
        
        LoadBalancer = WeightedRoundRobin(servers)
        
        weighted_servers: List[MockServer] = LoadBalancer.servers
        
        threads = []

        # TODO: a real load balancer proxy

        # proxy = Proxy(None, sorted_weighted_servers)
        # proxy_t = threading.Thread(target=proxy.process_requests, args=[num_of_clients])
        # proxy_t.start()

        sleep(1)

        # TODO: Add some logic to determine split between fast_response clients and normal clients.
        for _ in range(num_of_clients):
            client = MockClient()
            for _ in range(num_of_requests):
                server = LoadBalancer.get_next_server()
                if server is None:
                    continue
                
                print("server: ", server._server_address)
                # Capacity iteration is sent directly to request arg of client.
                t = threading.Thread(target=client.req, args=[server, server.weight])
                t.start()
                threads.append(t)

        for t in threads:
            t.join()
    
    
