import pandas as pd
import numpy as np
import os

rooms = ["Lab A", "Lab B", "Lab C", "Lab D", "Hall 1", "Hall 2", "Seminar Room 1", "Seminar Room 2", "Hostel A", "Hostel B"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
hours = list(range(8, 18))

capacities = {}
for r in rooms:
    if "Lab" in r:
        capacities[r] = 50
    elif "Hall" in r:
        capacities[r] = 150
    elif "Seminar" in r:
        capacities[r] = 60
    elif "Hostel" in r:
        capacities[r] = 200
    else:
        capacities[r] = 100

data = []

# Generate exactly 60 rows
for i in range(60):
    room = np.random.choice(rooms)
    day = np.random.choice(days)
    hour = int(np.random.choice(hours))
    start_time = f"{hour}:00"
    end_time = f"{hour+1}:00"
    subject = np.random.choice(["Physics", "Chemistry", "CS 101", "Math", "Biology", "Electronics", "Mechanics"])
    cap = capacities[room]
    
    if 8 <= hour <= 11:
        occ = np.random.uniform(0.6, 0.95)
    elif 14 <= hour <= 16:
        occ = np.random.uniform(0.05, 0.2)
    else:
        occ = np.random.uniform(0.1, 0.8)
    
    if np.random.random() < 0.3:
        occ = np.random.uniform(0.0, 0.15)
        
    students = int(cap * occ)
    occupancy = students / cap

    data.append([room, day, start_time, end_time, subject, students, cap, occupancy, hour])

df = pd.DataFrame(data, columns=["room", "day", "start_time", "end_time", "subject", "students", "capacity", "occupancy", "hour"])
os.makedirs("data", exist_ok=True)
df.to_csv("data/demo_timetable.csv", index=False)
print("demo_timetable.csv generated with 60 rows.")
