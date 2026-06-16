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
                      "remaining": burst_time,
                      "finish_time": 0,
                      "turnaround_time": 0,
                      "waiting_time": 0,})
    print()

# First Come First Serve (FCFS) Scheduling Algorithm
if choice == "1":
    print("First Come First Serve (FCFS) Scheduling Algorithm")
    
    processes.sort(key=lambda x: x["arrival"])  # Sort processes by arrival time

    current_time = 0
    gantt_chart = []

    for process in processes:
        if current_time < process["arrival"]:
                gantt_chart.append(("Idle", current_time, process["arrival"]))
                current_time = process["arrival"]
        start_time = current_time
        current_time += process["burst"]
        gantt_chart.append((process["process_id"], start_time, current_time))
        
        process["finish_time"]  = current_time
        process["turnaround_time"] = process["finish_time"] - process["arrival"]
        process["waiting_time"]  = process["turnaround_time"] - process["burst"]

    result = processes

# Non-Preemptive Shortest Job First (SJF) Scheduling Algorithm
elif choice == "2":
     print("Non-Preemptive Shortest Job First (SJF) Scheduling Algorithm")

     current_time = 0
     gantt_chart = []
     result = []
     remaining_processes = processes[:]

     while remaining_processes:
          available_processes = [process for process in remaining_processes if process["arrival"] <= current_time]
          if not available_processes:
               next_arrival = min(process["arrival"] for process in remaining_processes)
               gantt_chart.append(("Idle", current_time, next_arrival))
               current_time = next_arrival
               available_processes = [process for process in remaining_processes if process["arrival"] <= current_time]

          process = min(available_processes, key=lambda x: (x["burst"], x["arrival"]))
          remaining_processes.remove(process)
          start_time = current_time
          current_time += process["burst"]
          gantt_chart.append((process["process_id"], start_time, current_time))
          process["finish_time"]  = current_time
          process["turnaround_time"] = process["finish_time"] - process["arrival"]
          process["waiting_time"]  = process["turnaround_time"] - process["burst"]
          result.append(process)

# Print Gantt Chart
if gantt_chart:
    print("\nGantt Chart:")
    top =  "+"
    labels = "|"
    times = str(gantt_chart[0][1])

    for label, start, end in gantt_chart:
        width = end - start
        top += "-" * width + "+"
        labels += f"{label:^{width}}" + "|"
        times += f"{end:>{width}}"

    print(top)
    print(labels)
    print(top)
    print(times)
    
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
     

