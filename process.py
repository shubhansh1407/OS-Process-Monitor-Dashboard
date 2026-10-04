import time
import random
from enum import Enum
import uuid

class ProcessState(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"

class Process:
    def __init__(self, pid, name, priority):
        # PCB Information
        self.pid = pid
        self.name = name
        self.state = ProcessState.NEW
        self.priority = priority
        self.program_counter = 0
        self.cpu_registers = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
        self.memory_usage = random.randint(10, 1024) # MB
        self.io_status = "None"
        self.parent_pid = 1 # init process
        self.creation_time = time.strftime("%H:%M:%S")
        self.cpu_usage = 0 # simulated CPU time used
        self.total_burst_time = random.randint(10, 50)
        self.unique_id = str(uuid.uuid4())
