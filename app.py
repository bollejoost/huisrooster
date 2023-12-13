import os

import psycopg2
from sqlalchemy.exc import IntegrityError 
import time
from datetime import datetime, timedelta
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@login_required
def home():
    return render_template('layout.html')


def authenticate(name, password):
    conn = psycopg2.connect(
        host="localhost",
        database="huisrooster_db",
        user="bollejoost",
        password="password"
    )

    cur = conn.cursor()

    # Check if the name and password match a record in the users table
    cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if the entered name and password are valid
        user = authenticate(name, password)

        if user:
            # Successful login
            user_data = {'name': user[1], 'gang': user[3], 'admin': user[4], 'boete': user[5]}
            session['user'] = user_data
            print("User data:", user_data)  # debugging

            # Check if the user is an admin
            if user_data.get('admin'):
                return redirect(url_for('admin_dashboard'))  # go to admin dashboard
            else:
                return redirect(url_for('dashboard'))  # go to regular dashboard
        else:
            # Failed login
            error_message = 'Invalid name or password'
            print("Login failed:", error_message)  # Add this line for debugging
            return render_template('login.html', error_message=error_message)

    # render login for GET request
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page
    return redirect('/login')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Access user information from the session
    user = session.get('user')

    if not user:
        return redirect(url_for('login'))

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="huisrooster_db",
        user="bollejoost",
        password="password"
    )
    cur = conn.cursor()

    # Fetch the distinct weeks from the schedule
    cur.execute("SELECT DISTINCT week_id FROM schedule")
    weeks_data = cur.fetchall()
    weeks = sorted([week[0] for week in weeks_data])

    # Get the selected week from the form data
    selected_week = request.form.get('week')

    # Default to the first week if not selected
    if not selected_week:
        selected_week = weeks[0]

    # Set the initial date to January 3rd
    initial_date = datetime(datetime.now().year, 1, 3)

    # Calculate the week start date based on the selected week
    week_start_date = initial_date + timedelta(weeks=int(selected_week) - 1)

    # Fetch the schedule data for the selected week, including the 'is_done' column
    cur.execute("""
        SELECT schedule.task, users.name, schedule.is_done
        FROM schedule
        JOIN users ON schedule.assigned_user_id = users.id
        WHERE week_id = %s
    """, (selected_week,))
    schedule_data = cur.fetchall()

    # sort tasks
    tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
             "WC A", "WC B", "Keukenvloer", "Kookpitten", "Vuile was",
             "Gangen", "Papier en glas", "Ovens & balkon", "Vrij 1", "Vrij 2"]

    sorted_schedule_data = sorted(schedule_data, key=lambda x: tasks.index(x[0]))

    # Create a list of dictionaries to store the schedule data
    # Modify the schedule assignment in the 'dashboard' route
    schedule = {task: {'person': person, 'is_done': is_done} for task, person, is_done in sorted_schedule_data}

    # Calculate deadline dates for each week
    deadline_dates = [(week_start_date + timedelta(days=2, hours=23, minutes=59)).strftime("%d/%m") for week_start_date in
                      [initial_date + timedelta(weeks=int(week) - 1) for week in weeks]]

    # Close the database connection
    cur.close()
    conn.close()

    # Pass 'schedule', 'deadline_dates', 'weeks', 'selected_week', and 'week_start_date' to the template
    return render_template('dashboard.html', user=user, schedule=schedule, weeks=weeks, selected_week=selected_week, deadline_dates=deadline_dates, week_start_date=week_start_date)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    # Access user information from the session
    user = session.get('user')

    if not user:
        return redirect(url_for('login'))

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="huisrooster_db",
        user="bollejoost",
        password="password"
    )
    cur = conn.cursor()

    # Fetch the distinct weeks from the schedule
    cur.execute("SELECT DISTINCT week_id FROM schedule")
    weeks_data = cur.fetchall()
    weeks = sorted([week[0] for week in weeks_data])

    # Get the selected week from the form data
    selected_week = request.form.get('week')

    # Default to the first week if not selected
    if not selected_week:
        selected_week = weeks[0]

    # Set the initial date to January 3rd
    initial_date = datetime(datetime.now().year, 1, 3)

    # Calculate the week start date based on the selected week
    week_start_date = initial_date + timedelta(weeks=int(selected_week) - 1)

    # Fetch the schedule data for the selected week, including the 'is_done' column
    cur.execute("""
        SELECT schedule.task, users.name, schedule.is_done
        FROM schedule
        JOIN users ON schedule.assigned_user_id = users.id
        WHERE week_id = %s
    """, (selected_week,))
    schedule_data = cur.fetchall()

    # Sort tasks
    tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
             "WC A", "WC B", "Keukenvloer", "Kookpitten", "Vuile was",
             "Gangen", "Papier en glas", "Ovens & balkon", "Vrij 1", "Vrij 2"]

    sorted_schedule_data = sorted(schedule_data, key=lambda x: tasks.index(x[0]))

    # Create a list of dictionaries to store the schedule data
    schedule = {task: {'person': person, 'is_done': is_done} for task, person, is_done in sorted_schedule_data}

    # Calculate deadline dates for each week
    deadline_dates = [(week_start_date + timedelta(days=2, hours=23, minutes=59)).strftime("%d/%m") for week_start_date in
                      [initial_date + timedelta(weeks=int(week) - 1) for week in weeks]]

    # Fetch the users for the dropdowns
    cur.execute("SELECT name FROM users")
    users_data = cur.fetchall()
    users = [user[0] for user in users_data]

    # Handle form submission to switch users
    if request.method == 'POST':
        user1 = request.form.get('user1')
        print(f"Naam 1: {user1}")
        user2 = request.form.get('user2')
        print(f"Naam 2: {user2}")

        # Get the user IDs for the selected users
        cur.execute("SELECT id FROM users WHERE name = %s OR name = %s", (user1, user2))
        user_ids = cur.fetchall()
        user1_id, user2_id = user_ids[0][0], user_ids[1][0]

        # Switch assigned users in the database for the selected week
        cur.execute("""
            UPDATE schedule
            SET assigned_user_id = CASE
                WHEN assigned_user_id = %s THEN %s
                WHEN assigned_user_id = %s THEN %s
                ELSE assigned_user_id
            END
            WHERE week_id = %s
        """, (user1_id, user2_id, user2_id, user1_id, selected_week))

        conn.commit()


    # Close the database connection
    cur.close()
    conn.close()

    return render_template('admin.html', user=user, schedule=schedule, weeks=weeks, selected_week=selected_week, deadline_dates=deadline_dates, week_start_date=week_start_date, users=users)

@app.route('/confirm_task/<task>/<week>', methods=['POST'])
def confirm_task(task, week):
    # Access user information from the session
    user = session.get('user')

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="huisrooster_db",
        user="bollejoost",
        password="password"
    )
    cur = conn.cursor()

    try:
        # Update the 'is_done' field for the specified task and week
        cur.execute("UPDATE schedule SET is_done = TRUE WHERE task = %s AND week_id = %s AND assigned_user_id = (SELECT id FROM users WHERE name = %s)", (task, week, user['name']))

        # Commit the changes
        conn.commit()

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

    # Redirect back to the dashboard
    return redirect(url_for('dashboard'))   

if __name__ == '__main__':
    app.run(debug=True)
