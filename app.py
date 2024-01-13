import itertools
import time

class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.server_cycle = itertools.cycle(servers)

    def balance_request(self):
        # Get the next server in the round-robin cycle
        next_server = next(self.server_cycle)
        print(f"Redirecting request to Server {next_server}")

def simulate_requests(load_balancer, num_requests):
    for _ in range(num_requests):
        load_balancer.balance_request()
        time.sleep(1)  # Simulating processing time for each request

if __name__ == "__main__":
    # Define a list of server IDs (replace these with actual server addresses)
    server_list = [1, 2, 3, 4]

    # Create a LoadBalancer instance
    load_balancer = LoadBalancer(server_list)

    # Simulate requests being balanced by the load balancer
    simulate_requests(load_balancer, num_requests=10)
