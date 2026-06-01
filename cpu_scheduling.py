# Hello Ninjas

# First Come First Serve (FCFS) Scheduling Algorithm
processes = [{"process_id": "P1", "arrival": 0, "burst": 5}, 
             {"process_id": "P2", "arrival": 2, "burst": 3},
             {"process_id": "P3", "arrival": 4, "burst": 1},
             {"process_id": "P4", "arrival": 6, "burst": 2},
             {"process_id": "P5", "arrival": 8, "burst": 4}
             ]

current_time = 0

for process in processes:
   if current_time < process["arrival"]:
        current_time = process["arrival"]

   current_time += process["burst"]
  
   process["current_time"]  = current_time
   process["turnaround_time"] = process["current_time"] - process["arrival"]
   process["waiting_time"]  = process["turnaround_time"] - process["burst"]

print(f"{'Process ID':<10} {'Arrival Time':<10} {'Burst Time':<10} {'Current Time':<10} {'Turnaround Time':<10} {'Waiting Time':<10}")
print("-" * 75)
for process in processes:
    print(f"{process['process_id']:<13} {process['arrival']:<13} {process['burst']:<13} {process['current_time']:<13}  {process['turnaround_time']:<13}  {process['waiting_time']:<13}") 

# Compute for Average Waiting Time and Average Turnaround Time
total_processes = len(processes)
average_turnaround_time = sum(process["turnaround_time"] for process in processes) / total_processes
average_waiting_time = sum(process["waiting_time"] for process in processes) / total_processes
print(f"\nAverage Turnaround Time: {average_turnaround_time}")
print(f"Average Waiting Time: {average_waiting_time}")
