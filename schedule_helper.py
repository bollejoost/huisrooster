import random
import psycopg2

def create_schedule(names, tasks, db_connection):
    conn = psycopg2.connect(**db_connection)
    cur = conn.cursor()

    try:
        # Get the user IDs
        cur.execute("SELECT id FROM users WHERE name IN %s;", (tuple(names),))
        user_ids = [row[0] for row in cur.fetchall()]

        for week in range(1, 16):
            # Shuffle names for the current week
            random.shuffle(user_ids)

            # Insert schedules for the current week
            for task, user_id in zip(tasks, user_ids):
                cur.execute('''
                    INSERT INTO schedule (week_id, task, assigned_user_id)
                    VALUES (%s, %s, %s);
                ''', (week, task, user_id))

            conn.commit()

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

if __name__ == "__main__":
    names = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde",
             "Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]

    tasks = ["badkamer A", "badkamer B", "fusie", "huisboodschappen", "aanrecht",
             "WC A", "WC B", "keukenvloer", "kookpitten", "vuile was",
             "gangen", "papier en glas", "ovens & balkon", "vrij", "vrij"]

    db_connection = {
        'host': "localhost",
        'database': "huisrooster_db",
        'user': "bollejoost",
        'password': "password"
    }

    create_schedule(names, tasks, db_connection)
