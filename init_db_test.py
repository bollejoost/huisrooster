import os
import psycopg2
from schedule_helper import create_schedule

def main():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="huisrooster_db",
        user="bollejoost",  # Replace with your PostgreSQL username
        password="password"
    )

    cur = conn.cursor()

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

    # tasks list
    tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
             "WC A", "WC B", "Keukenvloer", "Kookpitten & vuilnisbakken", "Vuile was",
             "Gangen", "Papier en glas", "Ovens & balkon", "Vrij", "Vrij"]

    cur.execute('''
        CREATE TABLE schedule (
            week_id integer NOT NULL,
            task varchar(50) NOT NULL,
            is_done boolean DEFAULT false,
            assigned_user_id integer REFERENCES users(id)
        );

        INSERT INTO schedule (week_id, task) VALUES
        {week_values};
    '''.format(week_values=", ".join("(1, '{0}')".format(task) for task in tasks)))

    # Call the create_schedule function from the helper file
    names = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde",
             "Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]

    create_schedule(names, tasks, conn, cur)

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
