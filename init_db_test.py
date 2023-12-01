import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="huisrooster_db",
    user=os.environ['bollejoost'],
    password=os.environ['password']
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
cur.execute('DROP TABLE IF EXISTS schedule;')

cur.execute('''
    CREATE TABLE schedule (
        id serial PRIMARY KEY,
        task varchar(50) NOT NULL,
        is_done boolean DEFAULT false,
        assigned_user_id integer REFERENCES users(id)
    );

    INSERT INTO schedule (task, assigned_user_id) VALUES
    ('Badkamer A', 1), ('Badkamer B', 2), ('Fusie', 3), ('Huisboodschappen', 4),
    ('Aanrecht', 5), ('WC A', 6), ('WC B', 7), ('Keukenvloer', 8),
    ('Kookpitten & vuilnisbakken', 9), ('Vuile was', 10), ('Gangen', 11),
    ('Papier en glas', 12), ('Ovens & balkon', 13), ('Vrij', 14), ('Vrij', 15);
''')

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
