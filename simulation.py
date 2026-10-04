import time
import random
from process import Process, ProcessState
from scheduler import Scheduler

class Simulation:
    def __init__(self):
        self.processes = []
        self.events = []
        self.clock = 0
        self.is_running = False
        self.speed = 1.0
        self.next_pid = 100
        self.scheduler = Scheduler(algorithm="Priority")

    def init_processes(self, count=10):
        for _ in range(count):
            self.create_process()

    def get_process(self, pid):
        for p in self.processes:
            if p.pid == pid:
                return p
        return None

    def create_process(self):
        p = Process(self.next_pid, f"Proc_{self.next_pid}", random.randint(1, 10))
        self.processes.append(p)
        self.log_event(p.pid, p.name, "None", ProcessState.NEW.value, "Process Created")
        self.next_pid += 1

    def terminate_process(self, pid):
        p = self.get_process(pid)
        if p and p.state != ProcessState.TERMINATED:
            old_state = p.state
            p.state = ProcessState.TERMINATED
            self.log_event(p.pid, p.name, old_state.value, p.state.value, "Forced Termination")

    def log_event(self, pid, name, old_state, new_state, desc):
        self.events.insert(0, {
            "timestamp": time.strftime("%H:%M:%S"),
            "pid": pid,
            "process": name,
            "old_state": old_state,
            "new_state": new_state,
            "event": desc
        })
        if len(self.events) > 100:
            self.events = self.events[:100]

    def tick(self):
        if not self.is_running:
            return
        
        # 1. Handle currently RUNNING process
        running_processes = [p for p in self.processes if p.state == ProcessState.RUNNING]
        if running_processes:
            current_p = running_processes[0]
            current_p.cpu_usage += 1
            current_p.program_counter += random.randint(2, 8)
            current_p.cpu_registers = {k: random.randint(0, 255) for k in current_p.cpu_registers}
            
            # Check for termination
            if current_p.cpu_usage >= current_p.total_burst_time:
                current_p.state = ProcessState.TERMINATED
                self.log_event(current_p.pid, current_p.name, ProcessState.RUNNING.value, ProcessState.TERMINATED.value, "Execution Completed")
            else:
                # Random I/O Request
                if random.random() < 0.15:
                    current_p.state = ProcessState.WAITING
                    current_p.io_status = "Waiting for I/O"
                    self.log_event(current_p.pid, current_p.name, ProcessState.RUNNING.value, ProcessState.WAITING.value, "I/O Request")
                # Time Slice Expiration
                elif random.random() < 0.2:
                    current_p.state = ProcessState.READY
                    self.log_event(current_p.pid, current_p.name, ProcessState.RUNNING.value, ProcessState.READY.value, "Time Slice Expired")

        # 2. Handle NEW and WAITING processes
        for p in self.processes:
            if p.state == ProcessState.NEW:
                p.state = ProcessState.READY
                self.log_event(p.pid, p.name, ProcessState.NEW.value, ProcessState.READY.value, "Admitted to Ready Queue")
            elif p.state == ProcessState.WAITING:
                # I/O completion check
                if random.random() < 0.25:
                    p.state = ProcessState.READY
                    p.io_status = "None"
                    self.log_event(p.pid, p.name, ProcessState.WAITING.value, ProcessState.READY.value, "I/O Completed")

        # 3. Schedule next process if CPU is idle
        running_processes = [p for p in self.processes if p.state == ProcessState.RUNNING]
        if not running_processes:
            next_p = self.scheduler.select_next_process(self.processes)
            if next_p:
                next_p.state = ProcessState.RUNNING
                self.log_event(next_p.pid, next_p.name, ProcessState.READY.value, ProcessState.RUNNING.value, "Dispatched by Scheduler")

        self.clock += 1
