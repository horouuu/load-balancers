from ..main import *
from ..servers import GreenServer
import random

'''
    This Load Balancing algorithm uses 'weights' that the admin can assign to
    each server. It takes into account the weights of the server in order to
    decide the proportion of requests to send to each server. The server with
    greater 'weight' will be able to handle more requests compared to the server
    with less 'weight'.

    The weight itself is based on how "green" a server is. It will also prioritize
    servers of type GreenServer. The weight will also be updated per request as
    the carbon_emission of each server will change per request.

    Input: List of available servers.
    Output: A server that is not overloaded. It will prioritize green servers.
'''

# TODO: routing to green servers.
class GreenWeightedRoundRobin:
    class Server:
        def __init__(self, instance, weight):
            self.instance = instance
            self.weight = weight

        def get_instance(self):
            return self.instance

        def get_weight(self):
            return self.weight

    def __init__(self, servers):
        self.servers = servers[:]
        self.total_weight = sum(server.get_weight() for server in servers)
        self.cumulative_weights = self.calculate_cumulative_weights(servers)
        self.random = random.Random()

    def calculate_cumulative_weights(self, servers):
        cumulative_weights = [0] * len(servers)
        cumulative_weights[0] = servers[0].get_weight()
        for i in range(1, len(servers)):
            cumulative_weights[i] = cumulative_weights[i - 1] + servers[i].get_weight()
        return cumulative_weights

    def get_next_server(self):
        current_index = 0

        # Calculating random value for threshold. Note weight can now be a float.
        random_value = self.random.random() * max(self.cumulative_weights)

        # randomly choose a server (to send request)
        for i, weight in enumerate(self.cumulative_weights):
            if type(self.servers[i]) == GreenServer and random_value - weight < weight:
                current_index = i
                break
            if random_value < weight:
                current_index = i
                break
        return self.servers[current_index]
    