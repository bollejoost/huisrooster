import random
import os
import psycopg2

class Schedule:
    def __init__(self, names, tasks, db_connection):
        self.names = names
        self.tasks = tasks
        self.conn = psycopg2.connect(**db_connection)
        self.cur = self.conn.cursor()

        try:
            # Create the 'users' table
            self.cur.execute('DROP TABLE IF EXISTS users CASCADE;')

            self.cur.execute('''
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

            self.cur.executemany('''
                INSERT INTO users (name, password, gang, admin, boete) VALUES (%s, %s, %s, %s, %s);
            ''', people_data)

            # Create the 'schedule' table with default tasks
            self.cur.execute('DROP TABLE IF EXISTS schedule CASCADE;')

            self.cur.execute('''
                CREATE TABLE schedule (
                    week_id integer,
                    task varchar(50) NOT NULL,
                    is_done boolean DEFAULT false,
                    assigned_user_id integer REFERENCES users(id)
                );
            ''')

            # Create an instance of the Schedule class and generate the schedule
            self.schedule = Schedule(names, tasks, db_connection)
            self.schedule.generate_schedule()

            self.conn.commit()

        except Exception as e:
            print("Error:", e)

        finally:
            # Close the cursor and connection
            self.cur.close()
            self.conn.close()

class Schedule:
    def __init__(self, names, tasks, db_connection):
        self.names = names
        self.tasks = tasks
        self.db_connection = db_connection

    def generate_schedule(self):
        conn = psycopg2.connect(**self.db_connection)
        cur = conn.cursor()

        try:
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

            # Shuffle names for the first week
            random.shuffle(self.names)

            for week in range(1, 16):
                for person, task in zip(self.names, self.tasks):
                    # Insert schedules for the current week
                    cur.execute('''
                        INSERT INTO schedule (week_id, task, assigned_user_id)
                        VALUES (%s, %s, (SELECT id FROM users WHERE name = %s ORDER BY random() LIMIT 1));
                    ''', (week, task, person))

                # Rotate the names list for the next week
                self.names.append(self.names.pop(0))

        except Exception as e:
            print("Error:", e)

        finally:
            # Commit the changes and close the cursor and connection
            conn.commit()
            cur.close()
            conn.close()

if __name__ == "__main__":
    names = ["Maria", "Tim", "Samuel", "Jojanne", "Indrah", "Julian", "Linde",
             "Joost", "Emma", "Steven", "Knut", "Milan", "Pepijn", "Tessa", "Jolieke"]

    tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
             "WC A", "WC B", "Keukenvloer", "Kookpitten", "Vuile was",
             "Gangen", "Papier en glas", "Ovens & balkon", "Vrij 1", "Vrij 2"]

    db_connection = {
        'host': "localhost",
        'database': "huisrooster_db",
        'user': "bollejoost",
        'password': "password"
    }

    schedule_generator = Schedule(names, tasks, db_connection)
    schedule_generator.generate_schedule()
    