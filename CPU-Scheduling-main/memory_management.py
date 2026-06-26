# Memory Management and CPU Scheduling Simulation
# ==================================================


def print_title(title):
    print("\n" + title)
    print("=" * len(title))


def print_memory_map(segments, total_size):
    print_title("Memory Map")
    line = ""
    labels = ""
    for seg in segments:
        label = f"{seg['label']}({seg['size']})"
        width = max(len(label), 7)
        line += "+" + "-" * width
        labels += "|" + label.center(width)
    line += "+"
    labels += "|"
    print(line)
    print(labels)
    print(line)
    start = 0
    addr_line = f"{start:<6}"
    for seg in segments:
        width = max(len(f"{seg['label']}({seg['size']})"), 7)
        start += seg["size"]
        addr_line += f"{start:>{width + 1}}"
    print(addr_line)


def choose_memory_strategy():
    print_title("Memory Allocation Strategies")
    print("1. First Fit")
    print("2. Best Fit")
    print("3. Next Fit")
    print("4. Worst Fit")
    choice = input("Choose a memory allocation strategy (1-4): ").strip()
    return choice


def choose_cpu_scheduling():
    print_title("CPU Scheduling Algorithms")
    print("1. First Come First Serve (FCFS)")
    print("2. Non-Preemptive Shortest Job First (SJF)")
    print("3. Preemptive Shortest Job First (SJF)")
    print("4. Non-Preemptive Priority Scheduling")
    print("5. Preemptive Priority Scheduling")
    print("6. Round Robin (RR)")
    return input("Choose a CPU scheduling algorithm (1-6): ").strip()


def first_fit(free_blocks, request_size):
    for idx, block in enumerate(free_blocks):
        if block["size"] >= request_size:
            return idx
    return None


def best_fit(free_blocks, request_size):
    best_index = None
    best_size = None
    for idx, block in enumerate(free_blocks):
        if block["size"] >= request_size and (best_size is None or block["size"] < best_size):
            best_size = block["size"]
            best_index = idx
    return best_index


def worst_fit(free_blocks, request_size):
    worst_index = None
    worst_size = -1
    for idx, block in enumerate(free_blocks):
        if block["size"] >= request_size and block["size"] > worst_size:
            worst_size = block["size"]
            worst_index = idx
    return worst_index


def next_fit(free_blocks, request_size, last_index):
    if not free_blocks:
        return None, last_index
    n = len(free_blocks)
    for offset in range(n):
        idx = (last_index + offset) % n
        if free_blocks[idx]["size"] >= request_size:
            return idx, idx
    return None, last_index


def allocate_memory(processes, total_memory, strategy):
    free_blocks = [{"start": 0, "size": total_memory}]
    allocated_blocks = []
    last_fit_index = 0

    for process in processes:
        request_size = process["memory"]
        selected = None
        if strategy == "1":
            selected = first_fit(free_blocks, request_size)
        elif strategy == "2":
            selected = best_fit(free_blocks, request_size)
        elif strategy == "3":
            selected, last_fit_index = next_fit(free_blocks, request_size, last_fit_index)
        elif strategy == "4":
            selected = worst_fit(free_blocks, request_size)

        if selected is None:
            process["allocated"] = False
            continue

        block = free_blocks[selected]
        process["allocated"] = True
        process["start"] = block["start"]
        process["end"] = block["start"] + request_size
        allocated_blocks.append({
            "start": block["start"],
            "size": request_size,
            "label": process["id"],
            "pid": process["id"],
        })

        if block["size"] == request_size:
            free_blocks.pop(selected)
        else:
            free_blocks[selected] = {
                "start": block["start"] + request_size,
                "size": block["size"] - request_size,
            }

    free_blocks.sort(key=lambda x: x["start"])
    allocated_blocks.sort(key=lambda x: x["start"])
    segments = []
    next_addr = 0
    ai = 0
    fi = 0

    while next_addr < total_memory:
        next_alloc = allocated_blocks[ai] if ai < len(allocated_blocks) else None
        next_free = free_blocks[fi] if fi < len(free_blocks) else None
        if next_free and (not next_alloc or next_free["start"] < next_alloc["start"]):
            if next_free["start"] > next_addr:
                segments.append({"label": "Free", "size": next_free["start"] - next_addr})
                next_addr = next_free["start"]
            segments.append({"label": "Free", "size": next_free["size"]})
            next_addr += next_free["size"]
            fi += 1
        elif next_alloc:
            if next_alloc["start"] > next_addr:
                segments.append({"label": "Free", "size": next_alloc["start"] - next_addr})
                next_addr = next_alloc["start"]
            segments.append({"label": next_alloc["label"], "size": next_alloc["size"]})
            next_addr += next_alloc["size"]
            ai += 1
        else:
            break
    if next_addr < total_memory:
        segments.append({"label": "Free", "size": total_memory - next_addr})

    return segments, free_blocks


def schedule_fcfs(processes):
    processes = sorted(processes, key=lambda x: x["arrival"])
    current_time = 0
    gantt = []
    for process in processes:
        if current_time < process["arrival"]:
            gantt.append(("Idle", current_time, process["arrival"]))
            current_time = process["arrival"]
        gantt.append((process["id"], current_time, current_time + process["burst"]))
        current_time += process["burst"]
        process["finish"] = current_time
        process["turnaround"] = process["finish"] - process["arrival"]
        process["waiting"] = process["turnaround"] - process["burst"]
    return gantt


def schedule_sjf_nonpreemptive(processes):
    remaining = processes[:]
    current_time = 0
    gantt = []
    finished = []
    while remaining:
        available = [p for p in remaining if p["arrival"] <= current_time]
        if not available:
            next_arrival = min(p["arrival"] for p in remaining)
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue
        process = min(available, key=lambda x: (x["burst"], x["arrival"]))
        remaining.remove(process)
        gantt.append((process["id"], current_time, current_time + process["burst"]))
        current_time += process["burst"]
        process["finish"] = current_time
        process["turnaround"] = process["finish"] - process["arrival"]
        process["waiting"] = process["turnaround"] - process["burst"]
        finished.append(process)
    return gantt


def schedule_sjf_preemptive(processes):
    processes = [dict(p) for p in processes]
    for p in processes:
        p["remaining"] = p["burst"]
    current_time = 0
    gantt = []
    last = None
    start = 0
    remaining = processes[:]
    while remaining:
        available = [p for p in remaining if p["arrival"] <= current_time]
        if not available:
            next_arrival = min(p["arrival"] for p in remaining)
            if last is not None:
                gantt.append((last["id"], start, current_time))
                last = None
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            start = current_time
            continue
        current = min(available, key=lambda x: (x["remaining"], x["arrival"]))
        if current is not last:
            if last is not None:
                gantt.append((last["id"], start, current_time))
            start = current_time
            last = current
        current["remaining"] -= 1
        current_time += 1
        if current["remaining"] == 0:
            gantt.append((current["id"], start, current_time))
            current["finish"] = current_time
            current["turnaround"] = current["finish"] - current["arrival"]
            current["waiting"] = current["turnaround"] - current["burst"]
            remaining.remove(current)
            last = None
            start = current_time
    return gantt


def schedule_priority_nonpreemptive(processes):
    remaining = processes[:]
    current_time = 0
    gantt = []
    while remaining:
        available = [p for p in remaining if p["arrival"] <= current_time]
        if not available:
            next_arrival = min(p["arrival"] for p in remaining)
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue
        process = min(available, key=lambda x: (x["priority"], x["arrival"]))
        remaining.remove(process)
        gantt.append((process["id"], current_time, current_time + process["burst"]))
        current_time += process["burst"]
        process["finish"] = current_time
        process["turnaround"] = process["finish"] - process["arrival"]
        process["waiting"] = process["turnaround"] - process["burst"]
    return gantt


def schedule_priority_preemptive(processes):
    processes = [dict(p) for p in processes]
    for p in processes:
        p["remaining"] = p["burst"]
    current_time = 0
    gantt = []
    last = None
    start = 0
    remaining = processes[:]
    while remaining:
        available = [p for p in remaining if p["arrival"] <= current_time]
        if not available:
            next_arrival = min(p["arrival"] for p in remaining)
            if last is not None:
                gantt.append((last["id"], start, current_time))
                last = None
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            start = current_time
            continue
        current = min(available, key=lambda x: (x["priority"], x["arrival"]))
        if current is not last:
            if last is not None:
                gantt.append((last["id"], start, current_time))
            start = current_time
            last = current
        current["remaining"] -= 1
        current_time += 1
        if current["remaining"] == 0:
            gantt.append((current["id"], start, current_time))
            current["finish"] = current_time
            current["turnaround"] = current["finish"] - current["arrival"]
            current["waiting"] = current["turnaround"] - current["burst"]
            remaining.remove(current)
            last = None
            start = current_time
    return gantt


def schedule_round_robin(processes, time_quantum):
    processes = [dict(p) for p in processes]
    for p in processes:
        p["remaining"] = p["burst"]
    current_time = 0
    gantt = []
    queue = []
    i = 0
    n = len(processes)

    if n == 0:
        return gantt
    current_time = min(p["arrival"] for p in processes)
    while any(p["remaining"] > 0 for p in processes):
        while i < n and processes[i]["arrival"] <= current_time:
            queue.append(processes[i])
            i += 1
        if not queue:
            next_arrival = min(p["arrival"] for p in processes if p["arrival"] > current_time)
            gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            continue
        process = queue.pop(0)
        exec_time = min(time_quantum, process["remaining"])
        gantt.append((process["id"], current_time, current_time + exec_time))
        process["remaining"] -= exec_time
        current_time += exec_time
        while i < n and processes[i]["arrival"] <= current_time:
            queue.append(processes[i])
            i += 1
        if process["remaining"] > 0:
            queue.append(process)
        else:
            process["finish"] = current_time
            process["turnaround"] = process["finish"] - process["arrival"]
            process["waiting"] = process["turnaround"] - process["burst"]
    return gantt


def print_gantt_chart(gantt):
    if not gantt:
        return
    print_title("Gantt Chart")
    top = "+"
    labels = "|"
    times = f"{gantt[0][1]}"
    for label, start, end in gantt:
        width = max(len(label), 7)
        top += "-" * width + "+"
        labels += label.center(width) + "|"
        times += f"{end:>{width + 1}}"
    print(top)
    print(labels)
    print(top)
    print(times)


def print_scheduling_results(processes, gantt):
    print_gantt_chart(gantt)
    print_title("CPU Scheduling Results")
    print(f"{'Process':<10}{'Arrival':<10}{'Burst':<10}{'Priority':<10}{'Waiting':<10}{'Turnaround':<10}")
    print("-" * 60)
    total_wait, total_turnaround = 0, 0
    for process in processes:
        print(f"{process['id']:<10}{process['arrival']:<10}{process['burst']:<10}{process['priority']:<10}{process['waiting']:<10}{process['turnaround']:<10}")
        total_wait += process['waiting']
        total_turnaround += process['turnaround']
    count = len(processes)
    if count:
        print(f"\nAverage Waiting Time: {total_wait / count:.2f}")
        print(f"Average Turnaround Time: {total_turnaround / count:.2f}")


def main():
    print_title("Memory Management Simulation")
    total_memory = int(input("Enter total memory size: "))
    num_processes = int(input("Enter number of processes: "))

    processes = []
    for i in range(num_processes):
        pid = input(f"Enter Process ID for process {i + 1}: ")
        size = int(input(f"Enter memory requirement for {pid}: "))
        arrival = int(input(f"Enter arrival time for {pid}: "))
        burst = int(input(f"Enter CPU burst time for {pid}: "))
        priority = int(input(f"Enter priority for {pid} (lower is higher priority): "))
        processes.append({
            "id": pid,
            "memory": size,
            "arrival": arrival,
            "burst": burst,
            "priority": priority,
            "allocated": False,
            "start": None,
            "end": None,
        })

    strategy_choice = choose_memory_strategy()
    if strategy_choice not in {"1", "2", "3", "4"}:
        print("Invalid memory strategy choice. Exiting.")
        return

    segments, free_blocks = allocate_memory(processes, total_memory, strategy_choice)
    allocated = [p for p in processes if p["allocated"]]
    total_allocated = sum(p["memory"] for p in allocated)
    internal_frag = 0
    external_frag = sum(block["size"] for block in free_blocks)
    utilization = (total_allocated / total_memory) * 100 if total_memory else 0

    print_memory_map(segments, total_memory)
    print_title("Memory Statistics")
    print(f"Total memory size: {total_memory}")
    print(f"Allocated memory: {total_allocated}")
    print(f"Internal fragmentation: {internal_frag}")
    print(f"External fragmentation: {external_frag}")
    print(f"Memory utilization: {utilization:.2f}%")

    if not allocated:
        print("\nNo processes were allocated memory. CPU scheduling cannot be simulated.")
        return

    print_title("Allocated Processes")
    print(f"{'Process':<10}{'Memory':<10}{'Start':<10}{'End':<10}")
    print("-" * 40)
    for process in allocated:
        print(f"{process['id']:<10}{process['memory']:<10}{process['start']:<10}{process['end']:<10}")

    cpu_choice = choose_cpu_scheduling()
    scheduled_processes = [dict(p) for p in allocated]
    gantt = []
    if cpu_choice == "1":
        gantt = schedule_fcfs(scheduled_processes)
    elif cpu_choice == "2":
        gantt = schedule_sjf_nonpreemptive(scheduled_processes)
    elif cpu_choice == "3":
        gantt = schedule_sjf_preemptive(scheduled_processes)
    elif cpu_choice == "4":
        gantt = schedule_priority_nonpreemptive(scheduled_processes)
    elif cpu_choice == "5":
        gantt = schedule_priority_preemptive(scheduled_processes)
    elif cpu_choice == "6":
        quantum = int(input("Enter time quantum for Round Robin: "))
        gantt = schedule_round_robin(scheduled_processes, quantum)
    else:
        print("Invalid CPU scheduling choice. Exiting.")
        return

    print_scheduling_results(scheduled_processes, gantt)


if __name__ == "__main__":
    main()
