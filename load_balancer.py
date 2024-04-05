import collections
import threading
from typing import List
from clients import req
from servers import MockServer


class LoadBalancer: 
    def __init__(self):
        pass

    async def simulate_weighted_round_robin(weighted_servers: dict[MockServer, int], num_of_requests):
        sorted_weighted_servers = collections.OrderedDict(dict(
            sorted(
                weighted_servers.items(),
                key=lambda server: server[1],
                reverse=True)
            ))
        
        #TODO: create real clients AND a real load balancer proxy
        threads = []
        while (num_of_requests > 0):
            for server, weight in sorted_weighted_servers.items():
                for _ in range(weight):
                    print("server: ", server.server_address)
                    t = threading.Thread(target=req, args=[server])
                    threads.append(t)
                    num_of_requests -= 1
                    if num_of_requests < 0:
                        break

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    
    
