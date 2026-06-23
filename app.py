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


@app.route("/virtual-memory")
def virtual_memory():
    return render_template("coming_soon.html", title="Virtual Memory")


@app.route("/mass-storage-management")
def mass_storage_management():
    return render_template("coming_soon.html", title="Mass Storage Management")


if __name__ == "__main__":
    app.run(debug=True)
