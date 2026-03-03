from processes import load_processes


def run_fcfs():
    print("\n===== FCFS Simulation =====")

    processes = load_processes()
    ready_queue = processes[:]
    io_list = []

    current_time = 0
    cpu_busy_time = 0
    running = None

    while True:

        # Update I/O
        for p in io_list[:]:
            p.remaining_time -= 1
            if p.remaining_time == 0:
                p.move_to_next_burst()
                ready_queue.append(p)
                io_list.remove(p)

        # Schedule if CPU idle
        if running is None and ready_queue:
            running = ready_queue.pop(0)

            if running.response_time is None:
                running.response_time = current_time

            print(f"Time {current_time}: {running.pid} scheduled")

        # Run CPU
        if running:
            running.remaining_time -= 1
            cpu_busy_time += 1

            if running.remaining_time == 0:
                running.move_to_next_burst()

                if running.completed:
                    running.turnaround_time = current_time + 1
                    print(f"Time {current_time+1}: {running.pid} COMPLETED")
                else:
                    io_list.append(running)

                running = None

        # Update waiting times
        for p in ready_queue:
            p.waiting_time += 1

        current_time += 1

        if all(p.completed for p in processes):
            break

    print_results(processes, current_time, cpu_busy_time)


def print_results(processes, total_time, cpu_busy_time):
    print("\nFinal Results:")

    total_wait = 0
    total_turnaround = 0
    total_response = 0

    for p in processes:
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time

        print(f"{p.pid}: Tw={p.waiting_time}, "
              f"Ttr={p.turnaround_time}, "
              f"Tr={p.response_time}")

    n = len(processes)

    print("\nAverages:")
    print("CPU Utilization: {:.2f}%".format(
        (cpu_busy_time / total_time) * 100
    ))
    print("Avg Waiting Time:", total_wait / n)
    print("Avg Turnaround Time:", total_turnaround / n)
    print("Avg Response Time:", total_response / n)