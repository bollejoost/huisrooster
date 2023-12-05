import random

def create_schedule(names, tasks):
    schedule = {}

    # assign tasks randomly for first week
    random.shuffle(names)
    for task, name in zip(tasks, names):
        schedule[task] = name

    # print the first week
    print("Week 1 Schedule:")
    for task, name in schedule.items():
        print(f"{task}: {name}")
    print("\n")

    # rotate people over tasks for the next 14 weeks
    for week in range(2, 16):
        # Rotate the names
        names.insert(0, names.pop())

        # assign current week
        for task, name in zip(tasks, names):
            schedule[task] = name

        # print current week
        print(f"Week {week} Schedule:")
        for task, name in schedule.items():
            print(f"{task}: {name}")
        print("\n")

    return schedule

if __name__ == "__main__":
    names = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde",
             "Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]

    tasks = ["badkamer A", "badkamer B", "fusie", "huisboodschappen", "aanrecht",
             "WC A", "WC B", "keukenvloer", "kookpitten", "vuile was",
             "gangen", "papier en glas", "ovens & balkon", "vrij", "vrij"]

    schedule = create_schedule(names, tasks)
