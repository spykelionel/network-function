import itertools
import time

from asyncio import Event
from typing import Generic, List, NamedTuple, Type, TypeVar

queue = ['p1', 'p2', 'p3', 'p4', 'p5'] # Represents a list of processes

# Server state
class ServerState(NamedTuple):
    free = "free"
    normal = "normal"
    busy = "busy"
    pass

# Define type server
class Server(NamedTuple):
    name: str
    address: str
    load: float
    state: ServerState = ServerState.free


server1: Server = {
    'name': 'Neutron',
    'address': 'serv1',
    'load': 0.4,
    'state': ServerState.free
}

server2: Server = {
    'name': 'Muxyron',
    'address': 'serv2',
    'load': 0.24,
    'state': ServerState.free
}
server3: Server = {
    'name': 'Seluonx',
    'address': 'serv3',
    'load': 0.89,
    'state': ServerState.busy
}
server4: Server = {
    'name': 'Xaerin',
    'address': 'serv4',
    'load': 0.45,
    'state': ServerState.normal
}

server5: Server = {
    'name': 'Plusxin',
    'address': 'serv5',
    'load': 0.85,
    'state': ServerState.busy
}

# Now a list of servers
servers = [server1, server2, server3, server4, server5] 


class Scheduler:
    '''
    A simple round-robin scheduler
    '''
    def __init__(self, queue) -> None:
        self.processes = itertools.cycle(queue) # Hold on to the processes in the queue.
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

# An intelligent load balancer. Distributes load across servers base on their current state
class LoadBalancer:
    def __init__(self, servers):
        self.servers = itertools.cycle(servers)
        pass

    def balance_request(self):
        '''
        Get the next server in the round-robin cycle.
        If server is normal or free, pass the request on to the server.
        '''
        global servers
        next_server = next(self.servers)

        if next_server['state'] is ServerState.free or next_server['state'] is ServerState.normal:
            # For this scenario, let's say a request adds a 10% load to the server.
            print(f"Redirecting request to Server {next_server['name']}")
            index = servers.index(next_server)
            server = next_server
            server['load'] = float(server['load'])+.10
            servers.remove(next_server)
            servers.insert(index, server)
            print(f"Server state: {next_server['state']}")
            pass

def simulate_requests(load_balancer, num_requests):
    for _ in range(num_requests):
        load_balancer.balance_request()
        time.sleep(1)  # Simulating processing time for each request    

class Priority(NamedTuple):
    low = "low"
    high = "high"
    medium = "medium"
    pass

class Message(NamedTuple):
    action: str 
    payload: any  # payload should be generic. Type should be inferred at runtime
    events: List = []
    priority: Priority = Priority.low
    pass

todos = []
class Producer:
    messages: List[Message] = []

    def produce(self, message: Message):
        if(type(message) is not Message):
            raise TypeError("message must be of type message")
        self.messages.append(message)
        return
    def get(self):
        return itertools.cycle(self.messages)
    pass

T = TypeVar('T')

class Consumer(Generic[T]):
    def __init__(self, name, handler: Type[T]) -> None:
        print(f"Inititiating hanldler for {handler.__name__}")
        self.name = name
        self.handler = handler() # instantiate handler. Handler has args?
        pass

    def consume(self, message: Message):
        if message.action == "create":
            # Handle create actions here.
            self.handler.create(text=message.payload)
            Logger.log(f"Action {message.action} completed for {message}")
            pass

        elif message.action == "delete":
            # handle delete actions here
            self.handler.remove(message.payload)
            Logger.log(f"Action {message.action} completed for {message}")
            pass
        elif message.action == "get":
            # handle get action here.
            Todo.get()
            Logger.log(f"Action {message.action} completed for {message}")
            pass
        else:
            Logger.log(f"Action {message.action} Not found.")
            pass
        pass
    pass


class Todo:
    global todos
    def create(self, text):
        status = "success"
        try:
            todos.append(text)
            Logger.log(message=f"Todo({text}) has been created")
            status = "success"
        except:
            status = "failed"
            Logger.log(message=f"Unable to create Todo({text})")
            raise Exception("Can't create todo")
        
        return status
    
    def get(self):
        Logger.log(f"Returning all todos")
        return todos
    
    def get_single(self, idx):
        Logger.log(f"Returning Todo({idx})")
        return todos[idx]

    def remove(self, todo):
        Logger.log(f"Removing Todo({todo})")
        todos.remove(todo)
        return


class Logger:
    def log(message):
        # log to a file...
        print(message)

# Global producer
producer = Producer()

# global consumer
consumer = Consumer(name="Todo Consumer", handler=Todo)

if __name__ == "__main__":
    message = Message(action="create", payload="My todo")
    message2 = Message(action="create", payload="Second Todo")
    message3 = Message(action="create", payload="Last todo")
    message4 = Message(action="delete", payload="My todo")
    producer.produce(message)
    # producer.produce(message=message2)
    # producer.produce(message=message3)
    # producer.produce(message=message4)
    messages = itertools.cycle(producer.messages)
    
    # This task needs to be handled my a consumer e.g consumer.consume(message) in a list of messages
    for _ in range(len(producer.messages)):
        print(todos)
        m = next(messages)
        consumer.consume(message=m)

    print(todos)

