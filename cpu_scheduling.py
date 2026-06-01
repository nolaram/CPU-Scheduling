# Hello Ninjas

# First Come First Serve (FCFS) Scheduling Algorithm

processes = [{"pid": "P1", "arrival": 0, "burst": 5}, {"pid": "P2", "arrival": 2, "burst": 3},]

current_time = 0

for process in processes:
   if current_time < process["arrival"]:
        current_time = process["arrival"]

   current_time += process["burst"]
  
   process["ct"]  = current_time
   process["tat"] = process["ct"] - process["arrival"]
   process["wt"]  = process["tat"] - process["burst"]

for process in processes:
    print(f"{process['pid']}  CT={process['ct']}  TAT={process['tat']}  WT={process['wt']}") 