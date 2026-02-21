class Process:
    def __init__(self, pid, bursts):
        self.pid = pid
        self.bursts = bursts
        self.index = 0                 # current burst index
        self.remaining = bursts[0]     # remaining time in current burst

        self.waiting_time = 0
        self.response_time = None
        self.finish_time = None

        self.finished = False


def simulate_sjf(processes):
    time = 0
    cpu_busy = 0

    ready_queue = processes[:]   # all arrive at time 0
    io_list = []
    running = None

    while True:

        # -------------------------
        # 1. Check IO completion
        # -------------------------
        for p in io_list[:]:
            p.remaining -= 1
            if p.remaining == 0:
                p.index += 1
                if p.index < len(p.bursts):
                    p.remaining = p.bursts[p.index]
                    ready_queue.append(p)
                io_list.remove(p)

        # -------------------------
        # 2. If CPU idle → pick shortest job
        # -------------------------
        if running is None and ready_queue:
            running = min(ready_queue, key=lambda x: x.remaining)
            ready_queue.remove(running)

            # First time on CPU → response time
            if running.response_time is None:
                running.response_time = time

        # -------------------------
        # 3. Run CPU
        # -------------------------
        if running:
            running.remaining -= 1
            cpu_busy += 1

            if running.remaining == 0:
                running.index += 1

                if running.index < len(running.bursts):
                    # Go to IO
                    running.remaining = running.bursts[running.index]
                    io_list.append(running)
                else:
                    # Process finished
                    running.finish_time = time + 1
                    running.finished = True

                running = None

        # -------------------------
        # 4. Increase waiting time
        # -------------------------
        for p in ready_queue:
            p.waiting_time += 1

        # -------------------------
        # 5. Stop condition
        # -------------------------
        if all(p.finished for p in processes):
            break

        time += 1

    total_time = time + 1
    cpu_util = (cpu_busy / total_time) * 100

    return total_time, cpu_util


# -------------------------------------------------
# Process Data
# -------------------------------------------------

processes = [
    Process("P1", [5,27,3,31,5,43,4,18,6,22,4,26,3,24,4]),
    Process("P2", [4,48,5,44,7,42,12,37,9,76,4,41,9,31,7,43,8]),
    Process("P3", [8,33,12,41,18,65,14,21,4,61,15,18,14,26,5,31,6]),
    Process("P4", [3,35,4,41,5,45,3,51,4,61,5,54,6,82,5,77,3]),
    Process("P5", [16,24,17,21,5,36,16,26,7,31,13,28,11,21,6,13,3,11,4]),
    Process("P6", [11,22,4,8,5,10,6,12,7,14,9,18,12,24,15,30,8]),
    Process("P7", [14,46,17,41,11,42,15,21,4,32,7,19,16,33,10]),
    Process("P8", [4,14,5,33,6,51,14,73,16,87,6])
]

# Run simulation
total_time, cpu_util = simulate_sjf(processes)

# -------------------------------------------------
# Print Results
# -------------------------------------------------

print("\n===== SJF RESULTS =====\n")
print("Total Time to Complete All Processes:", total_time)
print("CPU Utilization: {:.2f}%".format(cpu_util))
print()

total_wait = 0
total_turnaround = 0
total_response = 0

for p in processes:
    turnaround = p.finish_time  # arrival time = 0

    total_wait += p.waiting_time
    total_turnaround += turnaround
    total_response += p.response_time

    print(p.pid)
    print("  Waiting Time:", p.waiting_time)
    print("  Turnaround Time:", turnaround)
    print("  Response Time:", p.response_time)
    print()

n = len(processes)

print("Average Waiting Time:", round(total_wait / n, 2))
print("Average Turnaround Time:", round(total_turnaround / n, 2))
print("Average Response Time:", round(total_response / n, 2))