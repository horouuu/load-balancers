from .dynamic_weighted_rr_prob import GreenWeightedRoundRobin
from .weighted_round_robin_prob import WeightedRoundRobin

# from ..servers import MockServer

import threading

from typing import List

import socket


"""
    Proxy class will be able to redirect traffic from clients to the adequate servers.
"""
class Proxy:
    
    def __init__(self
                 , loadbalancer: GreenWeightedRoundRobin | WeightedRoundRobin | None,
                 servers: List) -> None:
        self._load_balancer = loadbalancer
        self._servers = servers
    
        self._normal_servers, self._green_servers = self._separate_servers() 

    # Function will separate servers into green and mock servers.
    def _separate_servers(self) -> tuple:
        normal_servers = []
        green_servers = []

        for server in self._servers:
            if server.green == False:
                normal_servers.append(server)
            else:
                green_servers.append(server)
        
        return (normal_servers, green_servers)
    

    def _redirect_server(self, HTTP_request: str, new_server: str) -> str:
        splitted_data = HTTP_request.split('\r\n')   
        
        for i in range(len(splitted_data)):
            if "Host:" in splitted_data[i]:
                # Change to server.
                splitted_data[i] = f"Host: {new_server}"

        return '\r\n'.join(splitted_data)
    

    def _handle_client(self, client_socket: socket.socket):
        remote_host = "127.0.0.1"
        remote_port = 5006
        
        try:
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((remote_host, remote_port))

            print("Connected!")
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break


                # Modify response to new server
                redirected_data = self._redirect_server(data.decode('utf-8'), "127.0.0.1:5006")
                remote_socket.send(redirected_data.encode())

                remote_response = remote_socket.recv(4096)
                if not remote_response:
                    break

                client_socket.sendall(remote_response)
        
        finally:
            # Close both client and remote sockets when done
            client_socket.close()
            # remote_socket.close()


    # Intercept all HTML requests to all servers. Then use loadbalancer to determine.
    # Which server to direct request.
    def process_requests(self, num_clients: int):        
        local_host = "127.0.0.1"
        local_port = 8080
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((local_host, local_port))
        server_socket.listen(num_clients)
        
        print(f"[*] Listening on {local_host}:{local_port}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
            
            proxy_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
            proxy_thread.start()
        

