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
        user=os.environ['bollejoost'],
        password=os.environ['password']
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
            user_data = {'name': user[1], 'gang': user[3], 'admin': user[4], 'boete': user[5]}  # Adjust indices based on your actual user table structure
            session['user'] = user_data
            print("User data:", user_data)  # Add this line for debugging
            return redirect(url_for('dashboard'))  # Redirect to the dashboard route
        else:
            # Failed login
            error_message = 'Invalid name or password'
            print("Login failed:", error_message)  # Add this line for debugging
            return render_template('login.html', error_message=error_message)

    # If the request method is GET, simply render the login template
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page
    return redirect('/login')


@app.route('/dashboard')
# @login_required
def dashboard():
    # Access user information from the session
    user = session['user']

    if not user:
        return redirect(url_for('login'))

    schedule = {
        'Badkamer A': 'Linde',
        'Badkamer B': 'Tessa',
        'Fusie': 'Jojanne',
        'Huisboodschappen': 'Indrah',
        'Aanrecht': 'Milan',
        'WC A': 'Maria',
        'WC B': 'Pepijn',
        'Keukenvloer': 'Tim',
        'Kookpitten & vuilnisbakken': 'Jolieke',
        'Vuile was': 'Joost',
        'Gangen': 'Steven',
        'Papier en glas': 'Emma',
        'Vrij': 'Knut, Samuel, Julian'
    }
    
    # Check if the user is an admin
    if user.get('admin', False):
        # Render admin dashboard
        return render_template('admin.html', user=user, schedule=schedule)
    else:
        # Render regular user dashboard
        return render_template('dashboard.html', user=user, schedule=schedule)
    

if __name__ == '__main__':
    app.run(debug=True)
