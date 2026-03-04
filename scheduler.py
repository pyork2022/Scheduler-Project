from processes import load_processes


# =========================
# FCFS
# =========================
def run_fcfs():
    print("\n===== FCFS Simulation =====")

    processes = load_processes()
    ready_queue = processes[:]
    io_list = []

    current_time = 0
    cpu_busy_time = 0
    running = None

    while True:

        # Schedule if CPU idle
        if running is None and ready_queue:
            running = ready_queue.pop(0)

            if running.response_time is None:
                running.response_time = current_time

            print_dynamic_state(current_time, running, ready_queue, io_list)

        # Increment waiting time
        for p in ready_queue:
            p.waiting_time += 1

        # Run CPU
        if running:
            running.remaining_time -= 1
            cpu_busy_time += 1

        # Decrement I/O timers
        for p in io_list:
            p.remaining_time -= 1

        # Handle CPU completion
        if running and running.remaining_time == 0:
            running.move_to_next_burst()

            if running.completed:
                running.turnaround_time = current_time + 1
                print(f"\nTime {current_time+1}: {running.pid} COMPLETED")
            else:
                io_list.append(running)

            running = None

        # Move completed I/O back to ready queue
        for p in io_list[:]:
            if p.remaining_time == 0:
                p.move_to_next_burst()
                ready_queue.append(p)
                io_list.remove(p)

        current_time += 1

        if all(p.completed for p in processes):
            break

    print_results(processes, current_time, cpu_busy_time)


# =========================
# SJF (Non-Preemptive)
# =========================
def run_sjf():
    print("\n===== SJF Simulation =====")

    processes = load_processes()
    ready_queue = processes[:]
    io_list = []

    current_time = 0
    cpu_busy_time = 0
    running = None

    while True:

        # Move completed I/O to ready queue FIRST
        for p in io_list[:]:
            if p.remaining_time == 0:
                p.move_to_next_burst()
                ready_queue.append(p)
                io_list.remove(p)

        # Schedule if CPU idle
        if running is None and ready_queue:

            # Sort by shortest next CPU burst
            ready_queue.sort(key=lambda p: p.remaining_time)

            running = ready_queue.pop(0)

            if running.response_time is None:
                running.response_time = current_time

            print_dynamic_state(current_time, running, ready_queue, io_list)

        # Increment waiting time
        for p in ready_queue:
            p.waiting_time += 1

        # Run CPU
        if running:
            running.remaining_time -= 1
            cpu_busy_time += 1

        # Decrement I/O timers
        for p in io_list:
            p.remaining_time -= 1

        # Handle CPU completion
        if running and running.remaining_time == 0:
            running.move_to_next_burst()

            if running.completed:
                running.turnaround_time = current_time + 1
                print(f"\nTime {current_time+1}: {running.pid} COMPLETED")
            else:
                io_list.append(running)

            running = None

        # Advance time
        current_time += 1

        # Exit condition
        if all(p.completed for p in processes):
            break

    print_results(processes, current_time, cpu_busy_time)

# =========================
# MLFQ (3-Level)
# =========================
def run_mlfq():
    print("\n===== MLFQ Simulation =====")

    processes = load_processes()

    # Three queues
    q1 = processes[:]   # Highest priority
    q2 = []
    q3 = []

    io_list = []

    Q1 = 5
    Q2 = 10

    current_time = 0
    cpu_busy_time = 0
    running = None
    time_slice = 0

    while True:

        # Move completed I/O back to appropriate queue
        for p in io_list[:]:
            if p.remaining_time == 0:
                p.move_to_next_burst()
                p.queue_level = getattr(p, "queue_level", 1)

                if p.queue_level == 1:
                    q1.append(p)
                elif p.queue_level == 2:
                    q2.append(p)
                else:
                    q3.append(p)

                io_list.remove(p)

        # Preemption check (higher priority arrival)
        if running:
            if running.queue_level > 1 and q1:
                # Preempt to q2 or q3 front
                if running.queue_level == 2:
                    q2.insert(0, running)
                else:
                    q3.insert(0, running)
                running = None
                time_slice = 0

            elif running.queue_level == 3 and q2:
                q3.insert(0, running)
                running = None
                time_slice = 0

        # Schedule if CPU idle
        if running is None:

            if q1:
                running = q1.pop(0)
                running.queue_level = 1
                time_slice = Q1

            elif q2:
                running = q2.pop(0)
                running.queue_level = 2
                time_slice = Q2

            elif q3:
                running = q3.pop(0)
                running.queue_level = 3
                time_slice = float('inf')

            if running:
                if running.response_time is None:
                    running.response_time = current_time

                print_dynamic_state(
                    current_time,
                    running,
                    q1 + q2 + q3,
                    io_list
                )

        # Increment waiting time
        for p in (q1 + q2 + q3):
            p.waiting_time += 1

        # Run CPU
        if running:
            running.remaining_time -= 1
            cpu_busy_time += 1
            time_slice -= 1

        # Decrement I/O timers
        for p in io_list:
            p.remaining_time -= 1

        # CPU Burst Finished
        if running and running.remaining_time == 0:

            running.move_to_next_burst()

            if running.completed:
                running.turnaround_time = current_time + 1
                print(f"\nTime {current_time+1}: {running.pid} COMPLETED")
            else:
                io_list.append(running)

            running = None
            time_slice = 0

        # Time slice expired (demotion)
        elif running and time_slice == 0:

            if running.queue_level == 1:
                running.queue_level = 2
                q2.append(running)
            elif running.queue_level == 2:
                running.queue_level = 3
                q3.append(running)
            else:
                q3.append(running)

            running = None

        current_time += 1

        if all(p.completed for p in processes):
            break

    print_results(processes, current_time, cpu_busy_time)


# =========================
# Shared Dynamic Print
# =========================
def print_dynamic_state(current_time, running, ready_queue, io_list):
    print("\n----------------------------------------")
    print(f"Current Time: {current_time}")
    print(f"Running Process: {running.pid}")

    if ready_queue:
        print("Ready Queue: ", end="")
        print(", ".join(f"{p.pid}({p.remaining_time})" for p in ready_queue))
    else:
        print("Ready Queue: EMPTY")

    if io_list:
        print("I/O List: ", end="")
        print(", ".join(f"{p.pid}({p.remaining_time})" for p in io_list))
    else:
        print("I/O List: EMPTY")

    print("----------------------------------------")


# =========================
# Final Results
# =========================
def print_results(processes, total_time, cpu_busy_time):
    print("\n===== FINAL RESULTS =====")

    total_wait = 0
    total_turnaround = 0
    total_response = 0

    for p in processes:
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time

        print(f"{p.pid}: "
              f"Waiting={p.waiting_time}, "
              f"Turnaround={p.turnaround_time}, "
              f"Response={p.response_time}")

    n = len(processes)

    print("\n===== AVERAGES =====")
    print("Total completion time:", total_time)
    print("CPU Utilization: {:.2f}%".format(
        (cpu_busy_time / total_time) * 100
    ))
    print("Average Waiting Time:", total_wait / n)
    print("Average Turnaround Time:", total_turnaround / n)
    print("Average Response Time:", total_response / n)