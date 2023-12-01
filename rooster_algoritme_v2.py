import random

class Person:
    def __init__(self, name, gang):
        self.name = name
        self.gang = gang
        self.task_counts = {"Badkamer A": 0, "Badkamer B": 0, "Fusie": 0,
                            "Huisboodschappen": 0, "Aanrecht": 0, "WC A": 0,
                            "WC B": 0, "Keukenvloer": 0, "Kookpitten & vuilnisbakken": 0,
                            "Vuile was": 0, "Gangen": 0, "Papier en glas": 0,
                            "Ovens & balkon": 0, "Vrij": 0}

gang_a = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde"]
gang_b = ["Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]

people = []
for person_name in gang_a + gang_b:
    if person_name in gang_a:
        people.append(Person(person_name, "A"))
    else:
        people.append(Person(person_name, "B"))

tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
         "WC A", "WC B", "Keukenvloer", "Kookpitten & vuilnisbakken", "Vuile was",
         "Gangen", "Papier en glas", "Ovens & balkon", "Vrij", "Vrij"]

def assign_tasks(people, tasks):
    schedule = []
    
    for week in range(15):
        week_schedule = {}
        
        for person in people:
            available_tasks = [task for task in tasks if person.task_counts[task] < 1]
            
            if week == 0:
                assigned_task = random.choice(available_tasks)
            else:
                unassigned_tasks = [task for task in available_tasks if task not in week_schedule.values()]
                if unassigned_tasks:
                    assigned_task = random.choice(unassigned_tasks)
                else:
                    assigned_task = "Vrij"
                
            week_schedule[person.name] = assigned_task
            person.task_counts[assigned_task] += 1
        
        schedule.append(week_schedule)
    
    return schedule

# Example usage:
schedule = assign_tasks(people, tasks)
for week, week_schedule in enumerate(schedule):
    print(f"Week {week + 1}:")
    for person, task in week_schedule.items():
        print(f"  {person}: {task}")
