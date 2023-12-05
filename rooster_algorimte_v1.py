import random

# Define the people and tasks
gang_a = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde"]
gang_b = ["Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]
tasks = [
    "Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen",
    "Aanrecht", "WC A", "WC B", "Keukenvloer",
    "Kookpitten & vuilnisbakken", "Vuile was", "Gangen",
    "Papier en glas", "Ovens & balkon"
]

# Initialize a schedule dictionary to store assignments
schedule = {person: [] for person in gang_a + gang_b}

# Initialize a dictionary to track the tasks assigned each week
tasks_assigned_per_week = {person: set() for person in gang_a + gang_b}

# Generate the schedule
for week in range(1, 16):
    print(f"\nWeek {week} Schedule:")

    # Shuffle the order of people each week
    random.shuffle(gang_a)
    random.shuffle(gang_b)

    # Assign tasks to each person in gang_a
    for person in gang_a:
        # Ensure the person is not assigned more than once per week
        if len(schedule[person]) < 2:
            available_tasks = set(tasks) - tasks_assigned_per_week[person]
            if available_tasks:
                task = random.choice(list(available_tasks))
                schedule.setdefault(person, []).append((week, task))
                tasks_assigned_per_week[person].add(task)
                print(f"{person}: {task}")

    # Assign tasks to each person in gang_b
    for person in gang_b:
        # Ensure the person is not assigned more than once per week
        if len(schedule[person]) < 2:
            available_tasks = set(tasks) - tasks_assigned_per_week[person]
            if available_tasks:
                task = random.choice(list(available_tasks))
                schedule.setdefault(person, []).append((week, task))
                tasks_assigned_per_week[person].add(task)
                print(f"{person}: {task}")

# Print the final schedule
print("\nFinal Schedule:")
for person, assignments in schedule.items():
    print(f"{person}: {assignments}")

"""
maak persoon Class
- met lijst van taken die gedaan zijn
- 
"""