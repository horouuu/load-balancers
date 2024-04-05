
import asyncio
import collections
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
        while (num_of_requests > 0):
            for server, weight in sorted_weighted_servers.items():
                for _ in range(weight):
                    print("server: ", server.server_address)
                    asyncio.create_task(req(server))
                    num_of_requests -= 1
                    if num_of_requests < 0:
                        return
    
    
