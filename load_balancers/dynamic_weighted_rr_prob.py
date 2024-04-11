from servers import MockServer
from typing import List, Optional
import random

'''
    This Load Balancing algorithm uses 'weights' that the admin can assign to
    each server. It takes into account the weights of the server in order to
    decide the proportion of requests to send to each server. The server with
    greater 'weight' will be able to handle more requests compared to the server
    with less 'weight'.

    Input: List of available servers.
    Output: A server that is not overloaded. It will prioritize green servers.
'''

# TODO: routing to green servers.
class DynamicWeightedRoundRobin:
    class Server:
        def __init__(self, instance, weight):
            self.instance = instance
            self.weight = weight

        def get_instance(self):
            return self.instance

        def get_weight(self):
            return self.weight

    def __init__(self, servers):
        self.servers = self._assign_weights(servers[:])
        self.total_weight = sum(server.weight for server in servers)
        self.cumulative_weights = self.calculate_cumulative_weights(servers)
        self.random = random.Random()

    @staticmethod
    def _assign_weights( servers: List[MockServer]) -> dict[MockServer: int]:
        server_to_weight = {}
        for s in servers:
            s.weight = random.randint(1, len(servers))
            server_to_weight[s] = s.weight

        return server_to_weight

    def calculate_cumulative_weights(self, servers):
        cumulative_weights = [0] * len(servers)
        cumulative_weights[0] = servers[0].weight
        for i in range(1, len(servers)):
            cumulative_weights[i] = cumulative_weights[i - 1] + servers[i].weight
        return cumulative_weights

    def get_next_server(self) -> Optional[dict[MockServer, float]]:
        # randomly choose a server (to send request)
        random_value = int(self.random.random() * max(list(self.servers.values())))
        for server, weight in self.servers.items():
            if random_value < weight:
                return server, weight
        return None