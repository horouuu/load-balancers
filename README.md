# Usage:
1. Run `python3 servers.py` -- spins up 10 servers ranging from ports 5000 to 5009
2. Run `python3 clients.py` -- sends 10 HTTP GET requests to the 10 server instances and prints out their results as well as port

# TODO:
1. Log retransmission rate for each server
2. Log incoming requests/sent responses
3. Provide interface to include load balancing algorithm as a command argument to `servers.py`
