import random
import os
import psycopg2

def create_schedule(names, tasks, db_connection):
    conn = psycopg2.connect(**db_connection)
    cur = conn.cursor()

    try:
        # Create the 'users' table
        cur.execute('DROP TABLE IF EXISTS users CASCADE;')

        cur.execute('''
            CREATE TABLE users (
                id serial PRIMARY KEY,
                name varchar(100) NOT NULL,
                password varchar(100) NOT NULL,
                gang varchar(1) CHECK (gang IN ('A', 'B')) NOT NULL,
                admin boolean DEFAULT false,
                boete integer DEFAULT 0
            );
        ''')

        people_data = [
            ('Maria', 'Maria', 'A', False, 0),
            ('Tim', 'Tim', 'A', False, 0),
            ('Samuel', 'Samuel', 'A', False, 0),
            ('Jojanne', 'Jojanne', 'A', False, 0),
            ('Indrah', 'Indrah', 'A', False, 0),
            ('Julian', 'Julian', 'A', False, 0),
            ('Linde', 'Linde', 'A', False, 0),
            ('Joost', 'Joost', 'B', True, 0),  # Joost is an admin
            ('Emma', 'Emma', 'B', False, 0),
            ('Steven', 'Steven', 'B', False, 0),
            ('Knut', 'Knut', 'B', False, 0),
            ('Milan', 'Milan', 'B', False, 0),
            ('Pepijn', 'Pepijn', 'B', False, 0),
            ('Tessa', 'Tessa', 'B', False, 0),
            ('Jolieke', 'Jolieke', 'B', False, 0)
        ]

        cur.executemany('''
            INSERT INTO users (name, password, gang, admin, boete) VALUES (%s, %s, %s, %s, %s);
        ''', people_data)

        # Create the 'schedule' table with default tasks
        cur.execute('DROP TABLE IF EXISTS schedule CASCADE;')

        cur.execute('''
            CREATE TABLE schedule (
                week_id integer,
                task varchar(50) NOT NULL,
                is_done boolean DEFAULT false,
                assigned_user_id integer REFERENCES users(id)
            );
        ''')

        for week in range(1, 16):
            # Shuffle names for the current week
            random.shuffle(people_data)

            # Insert schedules for the current week
            for task, (_, _, gang, _, _) in zip(tasks, people_data):
                cur.execute('''
                    INSERT INTO schedule (week_id, task, assigned_user_id)
                    VALUES (%s, %s, (SELECT id FROM users WHERE gang = %s ORDER BY random() LIMIT 1));
                ''', (week, task, gang))

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
