import os

import psycopg2
from sqlalchemy.exc import IntegrityError 
import time
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
            print("User data:", user_data) # debugging
            return redirect(url_for('dashboard'))  # go to dashboard
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

    # Fetch the schedule data for the selected week
    cur.execute("SELECT task, name FROM schedule JOIN users ON schedule.assigned_user_id = users.id WHERE week_id = %s", (selected_week,))
    schedule_data = cur.fetchall()

    # sort tasks
    tasks = ["Badkamer A", "Badkamer B", "Fusie", "Huisboodschappen", "Aanrecht",
             "WC A", "WC B", "Keukenvloer", "Kookpitten", "Vuile was",
             "Gangen", "Papier en glas", "Ovens & balkon", "Vrij 1", "Vrij 2"]

    sorted_schedule_data = sorted(schedule_data, key=lambda x: tasks.index(x[0]))

    # Create a dictionary to store the schedule data
    schedule = {task: name for task, name in sorted_schedule_data}

    # Close the database connection
    cur.close()
    conn.close()

    # Render regular user dashboard with the updated schedule and weeks
    return render_template('dashboard.html', user=user, schedule=schedule, weeks=weeks, selected_week=selected_week)



if __name__ == '__main__':
    app.run(debug=True)
