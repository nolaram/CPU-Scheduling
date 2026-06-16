# CPU Scheduling Algorithms
# =========================

print("CPU Scheduling Algorithms")
print("-" * 25)
print("Select a CPU Scheduling Algorithm:")
print("1. First Come First Serve (FCFS)")
print("2. Non-Preemptive Shortest Job First (SJF)")

choice = input("Enter your desired CPU Scheduling Algorithm (1-2): ").strip()  

print()
number_of_processes = int(input("Enter the number of processes: "))

processes = []
for i in range(number_of_processes):
    process_id = input(f"Enter Process ID for Process {i + 1}: ")
    arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
    burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
    processes.append({"process_id": process_id, 
                      "arrival": arrival_time, 
                      "burst": burst_time,
                      "finish_time": 0,
                      "turnaround_time": 0,
                      "waiting_time": 0,})
    print()

# First Come First Serve (FCFS) Scheduling Algorithm

if choice == "1":
    print("First Come First Serve (FCFS) Scheduling Algorithm")
    
    processes.sort(key=lambda x: x["arrival"])  # Sort processes by arrival time

    current_time = 0

    for process in processes:
        if current_time < process["arrival"]:
                gantt_chart = f"Idle from {current_time} to {process['arrival']}"
                current_time = process["arrival"]
        start_time = current_time
        current_time += process["burst"]
        gantt_chart.append((process["process_id"], start_time, current_time))
        
        process["finish_time"]  = current_time
        process["turnaround_time"] = process["finish_time"] - process["arrival"]
        process["waiting_time"]  = process["turnaround_time"] - process["burst"]

    result = processes

# Computing Average Waiting Time and Average Turnaround Time     

if result:
    print(f"\n{'Process ID':<18}{'Arrival Time':<18}{'Burst Time':<18}{'Waiting Time':<18}{'Turnaround Time':<18}")
    print("-" * 90)
    for process in result:
        print(f"{process['process_id']:<18}{process['arrival']:<18}{process['burst']:<18}{process['waiting_time']:<18}{process['turnaround_time']:<18}")

    total = len(result)
    average_waiting_time = sum(p["waiting_time"] for p in result) / total
    average_turnaround_time = sum(p["turnaround_time"] for p in result) / total

    print(f"\nAverage Waiting Time: {average_waiting_time:.2f}")
    print(f"Average Turnaround Time: {average_turnaround_time:.2f}")
     

