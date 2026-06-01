# Hello Ninjas

# First Come First Serve (FCFS) Scheduling Algorithm
processes = [{"process_id": "P1", "arrival": 0, "burst": 5}, {"process_id": "P2", "arrival": 2, "burst": 3},]

current_time = 0

for process in processes:
   if current_time < process["arrival"]:
        current_time = process["arrival"]

   current_time += process["burst"]
  
   process["current_time"]  = current_time
   process["turnaround_time"] = process["current_time"] - process["arrival"]
   process["waiting_time"]  = process["turnaround_time"] - process["burst"]

for process in processes:
    print(f"{process['process_id']}  CT={process['current_time']}  TAT={process['turnaround_time']}  WT={process['waiting_time']}") 