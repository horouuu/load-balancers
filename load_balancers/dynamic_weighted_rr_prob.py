from servers import MockServer
from typing import List, Optional
import threading
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
        self.servers: List[MockServer] = servers[:]
        self.servers = sorted(servers, key= lambda server: server.weight)
        self.total_weight = sum(server.weight for server in servers)
        self.cumulative_weights = self.calculate_cumulative_weights(servers)
        self.random = random.Random()

    def assign_weights(self, is_fast_response: bool):

        # Base static weight on
        # Region.
        # Distance
        # Greeness

        singapore_weight = 4
        japan_weight = 3
        european_weight = 2
        us_weight = 1

        green_serv_weight = 3

        for s in self.servers:
            
            # Check region:
            region, latency = s.region
            
            if region == "Singapore":
                s.weight = singapore_weight
            elif region == "Tokyo":
                s.weight = japan_weight
            elif region == "Berlin":
                s.weight = european_weight
            elif region == "New York":
                s.weight = us_weight

            if s.green == True and not is_fast_response:
                s.weight += green_serv_weight

            s.weight += 1 / s.latency        

    def calculate_cumulative_weights(self, servers):
        cumulative_weights = [0] * len(servers)
        cumulative_weights[0] = servers[0].weight
        for i in range(1, len(servers)):
            cumulative_weights[i] = cumulative_weights[i - 1] + servers[i].weight
        return cumulative_weights

    def get_next_server(self) -> Optional[dict[MockServer, float]]:
        # randomly choose a server (to send request)
        random_value = int(self.random.random() * max([server.weight for server in self.servers]))
        for server in self.servers:
            if random_value < server.weight:
                self.servers.append(self.servers.pop(0))

                return server
        return None