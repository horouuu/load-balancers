import random

class WeightedRoundRobin:
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
        # randomly choose a server (to send request)
        random_value = self.random.randint(0, self.total_weight - 1)
        for i, weight in enumerate(self.cumulative_weights):
            if random_value < weight:
                current_index = i
                break
        return self.servers[current_index]