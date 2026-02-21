class Process:
    def __init__(self, pid, bursts):
        self.pid = pid
        self.bursts = bursts
        self.index = 0                 # which burst (CPU/IO)
        self.remaining = bursts[0]     # remaining time in current burst

        self.waiting_time = 0
        self.response_time = None
        self.finish_time = None

        self.started = False
        self.finished = False


def simulate_sjf(processes):
    time = 0
    cpu_busy = 0

    ready_queue = processes[:]   # all arrive at time 0
    io_list = []
    running = None

    while True:

        # 1. Check IO completion
        for p in io_list[:]:
            p.remaining -= 1
            if p.remaining == 0:
                p.index += 1
                if p.index < len(p.bursts):
                    p.remaining = p.bursts[p.index]
                    ready_queue.append(p)
                io_list.remove(p)

        # 2. If CPU idle → pick shortest job
        if running is None and ready_queue:
            running = min(ready_queue, key=lambda x: x.remaining)
            ready_queue.remove(running)

            if running.response_time is None:
                running.response_time = time

        # 3. Run CPU
        if running:
            running.remaining -= 1
            cpu_busy += 1

            if running.remaining == 0:
                running.index += 1

                if running.index < len(running.bursts):
                    # go to IO
                    running.remaining = running.bursts[running.index]
                    io_list.append(running)
                else:
                    running.finish_time = time
                    running.finished = True

                running = None

        # 4. Increase waiting time
        for p in ready_queue:
            p.waiting_time += 1

        # 5. Stop condition
        if all(p.finished for p in processes):
            break

        time += 1

    total_time = time
    cpu_util = (cpu_busy / total_time) * 100

    return total_time, cpu_util