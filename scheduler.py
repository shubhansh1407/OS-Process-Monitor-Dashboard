from process import ProcessState

class Scheduler:
    def __init__(self, algorithm="Priority"):
        self.algorithm = algorithm

    def select_next_process(self, processes):
        # Only ready processes can be scheduled
        ready_processes = [p for p in processes if p.state == ProcessState.READY]
        if not ready_processes:
            return None
        
        if self.algorithm == "Priority":
            # Higher priority number = higher priority
            return max(ready_processes, key=lambda p: p.priority)
        elif self.algorithm == "RoundRobin":
            return ready_processes[0]
        
        return ready_processes[0]
