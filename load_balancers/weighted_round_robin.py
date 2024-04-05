import random
from typing import List

from servers import MockServer

'''
    This Load Balancing algorithm uses 'weights' that the admin can assign to
    each server. It takes into account the weights of the server in order to
    decide the proportion of requests to send to each server. The server with
    greater 'weight' will be assigned the first # of requests

'''

# TODO: routing to green servers.
class WeightedRoundRobin:
    def assign_weights( servers: List[MockServer]) -> dict[MockServer: int]:
        server_to_weight = {}
        for s in servers:
            s.weight = random.randint(1, len(servers))
            server_to_weight[s] = s.weight

        return server_to_weight