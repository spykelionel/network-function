import itertools
import time

queue = ['p1', 'p2', 'p3', 'p4', 'p5'] # Represents a list of processes

class Scheduler:
    '''
    A simple round-robin scheduler
    '''
    def __init__(self, queue) -> None:
        self.processes = itertools.cycle(queue) # Hold on to the processes in the queue, return them one after the other.
        self.slice_time = 10 # Set the slice time or quantum time to 10ms 
        return None
    
    def exec(self): # Exec a process
        process = self.get_process()
        print(f"Executing process {process}")
        time.sleep(self.slice_time/10)
        return process

    def dispatch(self, process): # Dispatches a process after execution
        print(f"Dispatching process {process}")
        pass

    def get_process(self):
        return next(self.processes)


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
    # server_list = [1, 2, 3, 4]

    # # Create a LoadBalancer instance
    # load_balancer = LoadBalancer(server_list)

    # # Simulate requests being balanced by the load balancer
    # simulate_requests(load_balancer, num_requests=10)
    
    scheduler = Scheduler(queue)

    for i in range(len(queue)):
        process = scheduler.exec()
        scheduler.dispatch(process)
        

