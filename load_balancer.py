import collections
import threading
from typing import List, Dict
from clients import MockClient
from servers import MockServer
from load_balancers.weighted_round_robin_prob import WeightedRoundRobin
from load_balancers.dynamic_weighted_rr_prob import DynamicWeightedRoundRobin
from load_balancers.random import Random
from time import sleep

class LoadBalancer: 
    def __init__(self):
        pass

    async def simulate_weighted_round_robin(servers: List[MockServer], num_of_clients: int, num_of_requests: int, isDynamic: bool, fastResponse: bool, random: bool=False):
        
        if isDynamic:
            LoadBalancer = DynamicWeightedRoundRobin(servers)
        elif random:
            LoadBalancer = Random(servers)
        else:
            LoadBalancer = WeightedRoundRobin(servers)

        threads = []

        total_num_of_requests = num_of_clients * num_of_requests

        while total_num_of_requests > 0:
            client = MockClient(fastResponse)
            # Assign weights per client as weights depend on client fast_response.
            LoadBalancer.assign_weights(client.fast_response)

            server = LoadBalancer.get_next_server()

            for _ in range(int(server.weight)):
                t = threading.Thread(target=client.req, args=[server])
                t.start()
                threads.append(t)
                total_num_of_requests -= 1
                if total_num_of_requests == 0:
                    break
                # get next server should change to just sort after weights are updated 
            servers = sorted(servers, key=lambda server: server.weight, reverse=True)
            
        for t in threads:
            t.join()


        # # TODO: Add some logic to determine split between fast_response clients and normal clients.
        # for _ in range(num_of_clients):
        #     client = MockClient()
        #     for _ in range(num_of_requests):
        #         server = LoadBalancer.get_next_server()
    
        #         # Capacity iteration is sent directly to request arg of client.
        #         t = threading.Thread(target=client.req, args=[server])
        #         t.start()
        #         threads.append(t)

        # for t in threads:
        #     t.join()
    
    
