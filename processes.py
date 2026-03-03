class Process:
    def __init__(self, pid, bursts):
        self.pid = pid
        self.bursts = bursts[:]
        self.current_burst = 0
        self.remaining_time = bursts[0]

        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = None

        self.completed = False
        self.queue_level = 1
        self.quantum_used = 0

    def is_cpu_burst(self):
        return self.current_burst % 2 == 0

    def move_to_next_burst(self):
        self.current_burst += 1
        if self.current_burst < len(self.bursts):
            self.remaining_time = self.bursts[self.current_burst]
        else:
            self.completed = True


def load_processes():
    return [
        Process("P1", [5,27,3,31,5,43,4,18,6,22,4,26,3,24,4]),
        Process("P2", [4,48,5,44,7,42,12,37,9,76,4,41,9,31,7,43,8]),
        Process("P3", [8,33,12,41,18,65,14,21,4,61,15,18,14,26,5,31,6]),
        Process("P4", [3,35,4,41,5,45,3,51,4,61,5,54,6,82,5,77,3]),
        Process("P5", [16,24,17,21,5,36,16,26,7,31,13,28,11,21,6,13,3,11,4]),
        Process("P6", [11,22,4,8,5,10,6,12,7,14,9,18,12,24,15,30,8]),
        Process("P7", [14,46,17,41,11,42,15,21,4,32,7,19,16,33,10]),
        Process("P8", [4,14,5,33,6,51,14,73,16,87,6])
    ]