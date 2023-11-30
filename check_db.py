import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="huisrooster_db",
    user=os.environ['bollejoost'],
    password=os.environ['password']
)

cur = conn.cursor()

# Select all data from the users table
cur.execute('SELECT * FROM users;')
rows = cur.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
