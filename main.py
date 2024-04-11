import asyncio
from typing import List, Dict
from load_balancer import LoadBalancer
from servers import MockServer, create_servers
from time import time, sleep
from sys import argv
from math import ceil, floor
from clients import kill
NUM_CLIENTS = 1
NUM_REQUESTS = 720    # Note :: This will be PER CLIENT. if NUM_CLIENTS = 10 and NUM_REQUEST = 100; then
                    # total number of requests is 1000

# Dict allows us to allocate which server regions we would like to use and how many of those should be green.
SEVER_PARAMS: Dict[str, int] = {
    "US-1 Normal"       : 1,
    "US-1 Green"        : 0,

    "SG-1 Normal"       : 2,
    "SG-1 Green"        : 1,
    
    "JP-1 Normal"       : 1,
    "JP-1 Green"        : 3,
    
    "EU-1 Normal"       : 1,
    "EU-1 Green"        : 0,
}

if ("-no-lb" in argv):
    SEVER_PARAMS: Dict[str, int] = {
    "US-1 Normal"       : 1,
    "US-1 Green"        : 0,

    "SG-1 Normal"       : 2,
    "SG-1 Green"        : 1,
    
    "JP-1 Normal"       : 1,
    "JP-1 Green"        : 3,
    
    "EU-1 Normal"       : 1,
    "EU-1 Green"        : 0,
}

def main():
    asyncio.run(static_lb_simulation()) # Weighted Round Robin (Static) Load Balancer Algorithm

async def static_lb_simulation(): 
    isDynamic = "-dynamic" in argv
    nolb = "-no-lb" in argv
    fast_response = "-fast-response" in argv

    servers: List[MockServer] = create_servers(SEVER_PARAMS, isDynamic)
    t = time()
    await LoadBalancer.simulate_weighted_round_robin(servers, NUM_CLIENTS, NUM_REQUESTS, isDynamic, fast_response, nolb)
    t = time() - t
    total_power_usage = 0
    total_green = 0
    total_requests = 0
    total_inter = 0

    print("-------------------")
    print(f"Summary {'(Dynamic)' if isDynamic else ''}")
    print("-------------------")
    for server in sorted(servers, key= lambda s: s.weight, reverse=True):
        print(f'{server.region[0]}{"(Green)" if server.green else ""}:\nAverage response time: {server.avg_response_time} ms\nWeight: {server.weight}\nTotal # of requests: {server._total_requests}\n')
        total_green += server.green * server.total_requests
        total_requests += server.total_requests
        total_power_usage += server.trans_power_usage
        total_inter += (server.region[0] != "Singapore") * server.total_requests
    print("-------------------")
    print(f"Analytics {'(Dynamic)' if isDynamic else ''}")
    print("-------------------")
    print(f"Time taken: {t*1000} ms to complete {NUM_REQUESTS * NUM_CLIENTS} requests.\n")
    print(f"Total requests served: {total_requests}")
    print(f"Total power used in transmitting data: {total_power_usage/1000} kW.")
    print(f"Total green requests: {total_green} | {floor(total_green/total_requests * 100)}%")
    print(f"Total international requests: {total_inter} | {floor(total_inter/total_requests * 100)}%")

    if "-benchmark" not in argv:
        return
    
    idx = argv.index("-benchmark")
    bm_isDynamic = str(argv[idx+1]).lower() == "dynamic"
    print(f"-------------------\n\n\n")
    print(f"-------------------\n")
    print(argv)
    print(idx)
    if len(argv) < idx + 2:
        print("Missing benchmark type.")
        print("Available types: static, dynamic, no-lb")
        return
    
    print(f"Starting benchmark against: {argv[idx+1]}.")
    sleep(1)
    print(f"Killing all servers...")
    for server in servers:
        try:
            kill(server)
        except RuntimeError:
            print(f"Server at port {server.port} gracefully terminated.")

    print(f"All servers successfully killed. Restarting prodecures for benchmark: {argv[idx+1]}")
    sleep(2)

    # BENCHMARK
    bm_servers: List[MockServer] = create_servers(SEVER_PARAMS, bm_isDynamic)
    bm_t = time()
    await LoadBalancer.simulate_weighted_round_robin(bm_servers, NUM_CLIENTS, NUM_REQUESTS, bm_isDynamic, fast_response)
    bm_t = time() - bm_t
    bm_total_power_usage = 0
    bm_total_green = 0
    bm_total_requests = 0
    bm_total_inter = 0

    print("-------------------")
    print(f"BENCHMARK Summary {'(Dynamic)' if bm_isDynamic else ''}")
    print("-------------------")
    for bm_server in sorted(bm_servers, key= lambda s: s.weight, reverse=True):
        print(f'{bm_server.region[0]}{"(Green)" if bm_server.green else ""}:\nAverage response time: {bm_server.avg_response_time} ms\nWeight: {bm_server.weight}\nTotal # of requests: {bm_server._total_requests}\n')
        bm_total_green += bm_server.green * bm_server.total_requests
        bm_total_requests += bm_server.total_requests
        bm_total_power_usage += bm_server.trans_power_usage
        bm_total_inter += (bm_server.region[0] != "Singapore") * bm_server.total_requests
    print("-------------------")
    print(f"BENCHMARK Analytics {'(Dynamic)' if bm_isDynamic else ''}")
    print("-------------------")
    print(f"Time taken: {bm_t*1000} ms to complete {NUM_REQUESTS * NUM_CLIENTS} requests.\n")
    print(f"Total requests served: {bm_total_requests}")
    print(f"Total power used in transmitting data: {bm_total_power_usage/1000} kW.")
    print(f"Total green requests: {bm_total_green} | {floor(bm_total_green/bm_total_requests * 100)}%")
    print(f"Total international requests: {bm_total_inter} | {floor(bm_total_inter/bm_total_requests * 100)}%")
    print("-------------------")
    print(f"BENCHMARK Results {'Dynamic' if isDynamic else 'Static'} vs. {argv[idx+1]}")
    print("-------------------")
    print(f"Requests served: {total_requests} -> {bm_total_requests}")
    print(f"Time delta: {t*1000}ms -> {bm_t*1000}ms")
    print(f"Power delta: {total_power_usage/1000}kW -> {bm_total_power_usage/1000}kW")
    print(f"Green request delta: {total_green} | {floor(total_green/total_requests*100)}% -> {bm_total_green} | {floor(bm_total_green/total_requests * 100)}%")
    print(f"International delta: {total_inter} | {floor(total_inter/total_requests*100)}% -> {bm_total_inter} | {floor(bm_total_inter/bm_total_requests*100)}%")

if __name__ == "__main__": 
    main()