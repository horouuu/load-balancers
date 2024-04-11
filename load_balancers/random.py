from servers import MockServer
from typing import List, Optional
import random

'''
    chooses random server from server list
'''

class Random:
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
        self.servers = sorted(servers, key= lambda server: server.weight, reverse=True)

    def assign_weights(self, is_fast_response: bool):
        pass
            

    def calculate_cumulative_weights(self, servers):
        pass

    def get_next_server(self) -> Optional[dict[MockServer, float]]:
        next_server = self.servers[random.choice(range(0, len(self.servers)))]
        return next_server