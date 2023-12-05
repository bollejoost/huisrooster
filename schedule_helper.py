import random

def create_schedule(names, tasks, conn, cur):
    # Create an empty schedule dictionary
    schedule = {}

    # Insert tasks into the schedule for the first week
    for task in tasks:
        schedule[task] = names.pop(0)

    # Insert the first week into the database
    for task, name in schedule.items():
        cur.execute("INSERT INTO schedule (week_id, task, assigned_user_id) VALUES (1, %s, (SELECT id FROM users WHERE name = %s));", (task, name))

    # Commit the changes for the first week
    conn.commit()

    # Rotate names for the next 14 weeks
    for week in range(2, 16):
        # Rotate the names
        names.append(names.pop(0))

        # Clear the schedule dictionary
        schedule.clear()

        # Insert tasks for the current week
        for task in tasks:
            schedule[task] = names[0]

        # Insert the current week into the database
        for task, name in schedule.items():
            cur.execute("INSERT INTO schedule (week_id, task, assigned_user_id) VALUES (%s, %s, (SELECT id FROM users WHERE name = %s));", (week, task, name))

        # Commit the changes for the current week
        conn.commit()

if __name__ == "__main__":
    # Test data
    names = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde",
             "Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]

    tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
             "WC A", "WC B", "Keukenvloer", "Kookpitten & vuilnisbakken", "Vuile was",
             "Gangen", "Papier en glas", "Ovens & balkon", "Vrij", "Vrij"]

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="huisrooster_db",
        user="bollejoost",
        password="password"
    )

    cur = conn.cursor()

    # Call the create_schedule function
    create_schedule(names.copy(), tasks, conn, cur)

    # Close the cursor and connection
    cur.close()
    conn.close()
