# Hello Ninjas

# First Come First Serve (FCFS) Scheduling Algorithm

arrival = 0
burst = 5
current_time = 0

current_time += burst
completion = current_time

turnaround_time = completion - arrival
waiting_time = turnaround_time - burst

print(f"CT={completion}, TAT={turnaround_time}, WT={waiting_time}")