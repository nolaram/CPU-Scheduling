from collections import defaultdict
from flask import Flask, render_template, request
from memory_management import (
    allocate_memory,
    schedule_fcfs,
    schedule_sjf_nonpreemptive,
    schedule_sjf_preemptive,
    schedule_priority_nonpreemptive,
    schedule_priority_preemptive,
    schedule_round_robin,
)

app = Flask(__name__)

def parse_reference_string(text):
    return [int(token) for token in text.strip().split() if token.strip()]


def fifo_page_replacement(references, frames_count):
    frames = [None] * frames_count
    queue = []
    history = []
    hits = 0
    faults = 0
    events = []

    for ref in references:
        if ref in frames:
            hits += 1
            events.append("hit")
        else:
            faults += 1
            events.append("fault")
            if None in frames:
                index = frames.index(None)
            else:
                index = queue.pop(0)
            frames[index] = ref
            queue.append(index)
        history.append(frames.copy())

    return history, faults, hits, events


def optimal_page_replacement(references, frames_count):
    frames = [None] * frames_count
    history = []
    hits = 0
    faults = 0
    events = []

    for idx, ref in enumerate(references):
        if ref in frames:
            hits += 1
            events.append("hit")
        else:
            faults += 1
            events.append("fault")
            if None in frames:
                replace_index = frames.index(None)
            else:
                future = references[idx + 1 :]
                future_distances = []
                for page in frames:
                    if page is None:
                        future_distances.append(float("inf"))
                    elif page in future:
                        future_distances.append(future.index(page))
                    else:
                        future_distances.append(float("inf"))
                replace_index = int(max(range(frames_count), key=lambda i: future_distances[i]))
            frames[replace_index] = ref
        history.append(frames.copy())

    return history, faults, hits, events


def lru_page_replacement(references, frames_count):
    frames = [None] * frames_count
    last_used = {}
    history = []
    hits = 0
    faults = 0
    events = []

    for time, ref in enumerate(references):
        if ref in frames:
            hits += 1
            events.append("hit")
        else:
            faults += 1
            events.append("fault")
            if None in frames:
                replace_index = frames.index(None)
            else:
                victim = min(
                    [page for page in frames if page is not None],
                    key=lambda page: last_used.get(page, -1),
                )
                replace_index = frames.index(victim)
            frames[replace_index] = ref
        last_used[ref] = time
        history.append(frames.copy())

    return history, faults, hits, events


def lfu_page_replacement(references, frames_count):
    frames = [None] * frames_count
    counts = defaultdict(int)
    load_time = {}
    history = []
    hits = 0
    faults = 0
    events = []

    for time, ref in enumerate(references):
        counts[ref] += 1
        if ref in frames:
            hits += 1
            events.append("hit")
        else:
            faults += 1
            events.append("fault")
            if None in frames:
                replace_index = frames.index(None)
            else:
                victim = min(
                    [page for page in frames if page is not None],
                    key=lambda page: (counts[page], load_time.get(page, 0)),
                )
                replace_index = frames.index(victim)
            frames[replace_index] = ref
            load_time[ref] = time
        history.append(frames.copy())

    return history, faults, hits, events


def counting_based_page_replacement(references, frames_count):
    frames = [None] * frames_count
    counts = defaultdict(int)
    load_time = {}
    history = []
    hits = 0
    faults = 0
    events = []

    for time, ref in enumerate(references):
        counts[ref] += 1
        if ref in frames:
            hits += 1
            events.append("hit")
        else:
            faults += 1
            events.append("fault")
            if None in frames:
                replace_index = frames.index(None)
            else:
                victim = min(
                    [page for page in frames if page is not None],
                    key=lambda page: (counts[page], load_time.get(page, 0)),
                )
                replace_index = frames.index(victim)
            frames[replace_index] = ref
            load_time[ref] = time
        history.append(frames.copy())

    return history, faults, hits, events


def run_page_replacement(algorithm, references, frames_count):
    if algorithm == "FIFO":
        return fifo_page_replacement(references, frames_count)
    if algorithm == "Optimal":
        return optimal_page_replacement(references, frames_count)
    if algorithm == "LRU":
        return lru_page_replacement(references, frames_count)
    if algorithm == "LFU":
        return lfu_page_replacement(references, frames_count)
    if algorithm == "Counting":
        return counting_based_page_replacement(references, frames_count)
    return [], 0, 0, []


def parse_disk_queue(text):
    return [int(token) for token in text.strip().split() if token.strip()]


def compute_disk_path(head, requests):
    return [head] + requests


def service_fcfs(head, requests):
    return compute_disk_path(head, requests)


def service_sstf(head, requests):
    remaining = list(requests)
    current = head
    serviced = []
    while remaining:
        next_request = min(remaining, key=lambda r: abs(r - current))
        serviced.append(next_request)
        remaining.remove(next_request)
        current = next_request
    return compute_disk_path(head, serviced)


def service_scan(head, requests):
    requests_sorted = sorted(requests)
    left = [r for r in requests_sorted if r < head]
    right = [r for r in requests_sorted if r >= head]
    if not right:
        order = left[::-1]
    else:
        order = right + left[::-1]
    return compute_disk_path(head, order)


def service_cscan(head, requests):
    requests_sorted = sorted(requests)
    left = [r for r in requests_sorted if r < head]
    right = [r for r in requests_sorted if r >= head]
    if not right:
        order = left[::-1]
    else:
        order = right + left
    return compute_disk_path(head, order)


def service_look(head, requests):
    requests_sorted = sorted(requests)
    left = [r for r in requests_sorted if r < head]
    right = [r for r in requests_sorted if r >= head]
    if not right:
        order = left[::-1]
    else:
        order = right + left[::-1]
    return compute_disk_path(head, order)


def service_clook(head, requests):
    requests_sorted = sorted(requests)
    left = [r for r in requests_sorted if r < head]
    right = [r for r in requests_sorted if r >= head]
    if not right:
        order = left[::-1]
    else:
        order = right + left
    return compute_disk_path(head, order)


def compute_head_movement(path):
    return sum(abs(path[i] - path[i - 1]) for i in range(1, len(path)))


def normalize_disk_points(path, width_per_point=110, height=190, margin=30):
    min_val = min(path)
    max_val = max(path)
    value_range = max_val - min_val or 1
    points = []
    for idx, track in enumerate(path):
        x = 40 + idx * width_per_point
        y = margin + (max_val - track) / value_range * height
        points.append({"x": x, "y": y, "label": track})
    svg_width = 40 + len(path) * width_per_point
    return points, svg_width, min_val, max_val


def disk_schedule(algorithm, head, requests):
    if algorithm == "FCFS":
        return service_fcfs(head, requests)
    if algorithm == "SSTF":
        return service_sstf(head, requests)
    if algorithm == "SCAN":
        return service_scan(head, requests)
    if algorithm == "C-SCAN":
        return service_cscan(head, requests)
    if algorithm == "LOOK":
        return service_look(head, requests)
    if algorithm == "C-LOOK":
        return service_clook(head, requests)
    return compute_disk_path(head, requests)

ALGORITHM_LABELS = {
    "1": "First Come First Serve (FCFS)",
    "2": "Non-Preemptive Shortest Job First (SJF)",
    "3": "Preemptive Shortest Job First (SJF)",
    "4": "Non-Preemptive Priority Scheduling",
    "5": "Preemptive Priority Scheduling",
    "6": "Round Robin (RR)",
}

MEMORY_STRATEGY_LABELS = {
    "1": "First Fit",
    "2": "Best Fit",
    "3": "Next Fit",
    "4": "Worst Fit",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cpu-scheduling", methods=["GET", "POST"])
def cpu_scheduling():
    if request.method == "POST":
        algorithm = request.form.get("algorithm")
        quantum = request.form.get("quantum", type=int)
        process_ids = request.form.getlist("pid[]")
        arrivals = request.form.getlist("arrival[]")
        bursts = request.form.getlist("burst[]")
        priorities = request.form.getlist("priority[]")

        processes = []
        for pid, arrival, burst, priority in zip(process_ids, arrivals, bursts, priorities):
            if not pid.strip() or not arrival.strip() or not burst.strip():
                continue
            processes.append({
                "id": pid.strip(),
                "arrival": int(arrival),
                "burst": int(burst),
                "priority": int(priority) if priority.strip() else 0,
            })

        gantt = []
        scheduled = []
        average_wait = 0
        average_turn = 0
        if processes:
            if algorithm == "1":
                gantt = schedule_fcfs(processes)
                scheduled = processes
            elif algorithm == "2":
                gantt = schedule_sjf_nonpreemptive(processes)
                scheduled = processes
            elif algorithm == "3":
                gantt = schedule_sjf_preemptive(processes)
                scheduled = processes
            elif algorithm == "4":
                gantt = schedule_priority_nonpreemptive(processes)
                scheduled = processes
            elif algorithm == "5":
                gantt = schedule_priority_preemptive(processes)
                scheduled = processes
            elif algorithm == "6":
                gantt = schedule_round_robin(processes, quantum or 1)
                scheduled = processes

            if scheduled:
                average_wait = sum(p.get("waiting", 0) for p in scheduled) / len(scheduled)
                average_turn = sum(p.get("turnaround", 0) for p in scheduled) / len(scheduled)

        total_time = gantt[-1][2] if gantt else 0
        bars = [
            {
                "label": label,
                "start": start,
                "end": end,
                "duration": end - start,
                "width": ((end - start) / total_time * 100) if total_time else 0,
            }
            for label, start, end in gantt
        ]

        return render_template(
            "result_cpu.html",
            algorithm_label=ALGORITHM_LABELS.get(algorithm, "Unknown"),
            scheduled=scheduled,
            gantt=bars,
            total_time=total_time,
            average_wait=average_wait,
            average_turn=average_turn,
            algorithm=algorithm,
        )

    return render_template("cpu_scheduling.html")


@app.route("/memory-management", methods=["GET", "POST"])
def memory_management():
    if request.method == "POST":
        total_memory = request.form.get("total_memory", type=int)
        strategy = request.form.get("strategy")
        algorithm = request.form.get("algorithm")
        quantum = request.form.get("quantum", type=int)
        process_ids = request.form.getlist("pid[]")
        memories = request.form.getlist("memory[]")
        arrivals = request.form.getlist("arrival[]")
        bursts = request.form.getlist("burst[]")
        priorities = request.form.getlist("priority[]")

        processes = []
        for pid, mem, arrival, burst, priority in zip(process_ids, memories, arrivals, bursts, priorities):
            if not pid.strip() or not mem.strip() or not arrival.strip() or not burst.strip():
                continue
            processes.append({
                "id": pid.strip(),
                "memory": int(mem),
                "arrival": int(arrival),
                "burst": int(burst),
                "priority": int(priority) if priority.strip() else 0,
                "allocated": False,
                "start": None,
                "end": None,
            })

        segments, free_blocks = allocate_memory(processes, total_memory, strategy)
        allocated = [p for p in processes if p["allocated"]]
        total_allocated = sum(p["memory"] for p in allocated)
        external_frag = sum(block["size"] for block in free_blocks)
        utilization = (total_allocated / total_memory * 100) if total_memory else 0

        schedule_gantt = []
        scheduled = []
        average_wait = 0
        average_turn = 0
        if allocated and algorithm:
            scheduled = [{**p} for p in allocated]
            if algorithm == "1":
                schedule_gantt = schedule_fcfs(scheduled)
            elif algorithm == "2":
                schedule_gantt = schedule_sjf_nonpreemptive(scheduled)
            elif algorithm == "3":
                schedule_gantt = schedule_sjf_preemptive(scheduled)
            elif algorithm == "4":
                schedule_gantt = schedule_priority_nonpreemptive(scheduled)
            elif algorithm == "5":
                schedule_gantt = schedule_priority_preemptive(scheduled)
            elif algorithm == "6":
                schedule_gantt = schedule_round_robin(scheduled, quantum or 1)
            if scheduled:
                average_wait = sum(p.get("waiting", 0) for p in scheduled) / len(scheduled)
                average_turn = sum(p.get("turnaround", 0) for p in scheduled) / len(scheduled)

        memory_bars = [
            {
                "label": seg["label"],
                "size": seg["size"],
                "width": seg["size"] / total_memory * 100 if total_memory else 0,
            }
            for seg in segments
        ]
        total_time = schedule_gantt[-1][2] if schedule_gantt else 0
        gantt_bars = [
            {
                "label": label,
                "start": start,
                "end": end,
                "duration": end - start,
                "width": ((end - start) / total_time * 100) if total_time else 0,
            }
            for label, start, end in schedule_gantt
        ]

        return render_template(
            "result_memory.html",
            strategy_label=MEMORY_STRATEGY_LABELS.get(strategy, "Unknown"),
            algorithm_label=ALGORITHM_LABELS.get(algorithm, "None"),
            total_memory=total_memory,
            allocated=allocated,
            free_blocks=free_blocks,
            segments=memory_bars,
            total_allocated=total_allocated,
            external_frag=external_frag,
            utilization=utilization,
            scheduled=scheduled,
            gantt=gantt_bars,
            average_wait=average_wait,
            average_turn=average_turn,
        )

    return render_template("memory_management.html")


@app.route("/virtual-memory", methods=["GET", "POST"])
def virtual_memory():
    if request.method == "POST":
        algorithm = request.form.get("vm_algorithm")
        reference_string = request.form.get("reference_string", "")
        frames_count = request.form.get("frames", type=int)

        references = parse_reference_string(reference_string)
        history, faults, hits, events = run_page_replacement(algorithm, references, frames_count or 0)

        frame_table = []
        for frame_idx in range(frames_count or 0):
            frame_row = [row[frame_idx] if frame_idx < len(row) else None for row in history]
            frame_table.append(frame_row)

        return render_template(
            "result_virtual_memory.html",
            algorithm=algorithm,
            reference_string=references,
            frames_count=frames_count,
            frame_table=frame_table,
            faults=faults,
            hits=hits,
            events=events,
        )

    return render_template("virtual_memory.html")


@app.route("/mass-storage-management", methods=["GET", "POST"])
def mass_storage_management():
    if request.method == "POST":
        algorithm = request.form.get("disk_algorithm")
        head = request.form.get("head", type=int)
        disk_queue_text = request.form.get("disk_queue", "")
        requests = parse_disk_queue(disk_queue_text)

        path = disk_schedule(algorithm, head, requests)
        total_movement = compute_head_movement(path)
        points, svg_width, min_track, max_track = normalize_disk_points(path)
        polyline_points = " ".join(f"{int(p['x'])},{int(p['y'])}" for p in points)

        return render_template(
            "result_mass_storage.html",
            algorithm=algorithm,
            head=head,
            disk_queue=requests,
            path=path,
            total_movement=total_movement,
            points=points,
            polyline_points=polyline_points,
            svg_width=svg_width,
            min_track=min_track,
            max_track=max_track,
        )

    return render_template("mass_storage_management.html")


if __name__ == "__main__":
    app.run(debug=True)
