import collections
import threading
from typing import List
from clients import MockClient
from servers import MockServer


class LoadBalancer: 
    def __init__(self):
        pass

    async def simulate_weighted_round_robin(weighted_servers: dict[MockServer, int], num_of_clients: int, num_of_requests: int):
        sorted_weighted_servers = collections.OrderedDict(dict(
            sorted(
                weighted_servers.items(),
                key=lambda server: server[1],
                reverse=True)
            ))
        
        #TODO: create real clients AND a real load balancer proxy
        threads = []
        # while (num_of_requests > 0):
        #     for server, weight in sorted_weighted_servers.items():
        #         for _ in range(weight):
        #             print("server: ", server.server_address)
        #             t = threading.Thread(target=req, args=[server])
        #             threads.append(t)
        #             num_of_requests -= 1
        #             if num_of_requests < 0:
        #                 break

        # TODO: Add some logic to determine split between fast_response clients and normal clients.
        for _ in range(num_of_clients):
            client = MockClient()
            for server, weight in sorted_weighted_servers.items():
                print("server: ", server.server_address)
                # Capacity iteration is sent directly to request arg of client.
                t = threading.Thread(target=client.req, args=[server, weight])
                threads.append(t)
                num_of_requests -= weight
                if num_of_requests <= 0:
                    break


        for t in threads:
            t.start()

        for t in threads:
            t.join()

    
    
