import re
import tkinter

import mysql.connector
from bleach import clean
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator

# Starts app and initializes secret key
app = Flask(__name__)
app.secret_key = "12345"

# Database connection
db = mysql.connector.connect(host='localhost', user='root', password='', database='login', port=3306)


@app.route('/')
def index():
    # Checks if user is logged in
    if 'username' in session:
        # User is logged in show them the home page
        return render_template('home.html')
    # User is not logged in, then redirect to login page
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Checks if user is logged in
    if 'username' in session:
        # User is logged in show them the home page
        return render_template('home.html')
    if request.method == "POST":
        # Check if "username" and "password" exist in user submitted form
        if "Username" in request.form and "Password" in request.form:
            # Create variables for easy access of the username, and password
            username = request.form['Username']
            password = request.form['Password']
            # Initializes database connection
            database = mysql.connector.connect(host='localhost', user='root', database='login')
            cursor = database.cursor(dictionary=True)
            # Selects everything from database where username and password have user data
            select = 'SELECT * FROM login.login WHERE username=%s and password=%s'
            values = (username, password)
            cursor.execute(select, values)
            # Fetch one record and return result
            account = cursor.fetchone()
            if account:
                # Create session data, we can access this data in other routes
                session['logged'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['name'] = account['name']
                # Account is logged in and moved to the home page
                print('Logged in successfully !')
                return redirect(url_for('parts'))
            else:
                # Account doesnt exist or username/password incorrect and redirected to login page again
                print("Incorrect")
                return render_template('login.html')
        return render_template('login.html')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def new_user():
    # Checks if user is logged in
    if 'username' in session:
        # User is logged in show them the home page
        return render_template('home.html')
    if request.method == "POST":
        # Check if "name", "username" and "password" exist in the user submitted form
        if "Name" in request.form and "Username" in request.form and "Password" in request.form:
            # Create variables for easy access of the name, username, and password
            name = request.form['Name']
            username = request.form['Username']
            password = request.form['Password']
            # Initializes database connection
            database = mysql.connector.connect(host='localhost', user='root', database='login')
            cursor = database.cursor(dictionary=True)
            # Selecting everything from database of the username
            cursor.execute('SELECT * FROM login.login WHERE username=%s', (username,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                print("account already exists")
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', username):
                print('Invalid email address !')
            elif not re.match(r'[A-Za-z0-9]+', name):
                print('Username must contain only characters and numbers !')
            elif not name or not password or not username:
                print('Please fill out the form !')
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                insert = 'INSERT INTO login.login (`name`, `username`, `password`) VALUES (%s, %s, %s)'
                values = (name, username, password)
                cursor.execute(insert, values)
                database.commit()
                print("Successfully registered")
                return redirect(url_for("index"))
        elif request.method == 'POST':
            print("fill out the form")
            return render_template('register.html')
    return render_template('register.html')


@app.route('/parts', methods=['GET', 'POST'])
def parts():
    dbm = DatabaseManipulator()
    dbc = DatabaseConnector()
    results = dbm.fetchall()
    webui_host = dbc.get_webui_host()
    van_nums = dbm.get_van_nums()
    if request.method == 'POST':
        # Sanitizes the input using bleach
        part_name = clean(request.form['partName'])
        part_number = clean(request.form['partNumber'])
        van_number = clean(request.form['van'])
        # Insert into the database
        dbm.insert(part_name=part_name, part_number=part_number, van_number=van_number)
    return render_template('index.html', results=results, webui_host=webui_host, van_nums=van_nums)


# Displays the table code in table.html so it can be refreshed dynamically without reloading the page
@app.route('/table/<table_name>/<van_number>/', methods=['GET', 'POST'])
def table(table_name, van_number):
    dbm = DatabaseManipulator()
    # Requirements to return the results for a van by its number
    if table_name == 'vans' and van_number != 'all':
        results = dbm.get_vans(van_number)
        return render_template('van_table.html', results=results)
    # Requirements to return the master list of parts
    elif table_name == 'main' and van_number == 'all':
        results = dbm.fetchall()
        van_nums = dbm.get_van_nums()
        return render_template('table.html', results=results, van_nums=van_nums)
    # If the url is attempted to be accessed, redirect to index
    else:
        return redirect(url_for('parts'))


# Route for the delete method
@app.route('/delete/', methods=['POST', 'GET'])
def delete():
    dbm = DatabaseManipulator()
    if request.method == 'POST':
        part_id = request.form.get('Delete')
        dbm.delete(part_id)
    # If the /delete route is accessed, re-route to index
    return redirect(url_for('parts'))


# Route to edit table rows using the update method
@app.route('/update/', methods=['POST', 'GET'])
def update():
    dbm = DatabaseManipulator()
    if request.method == 'POST':
        part_id = request.form.get('id')
        part_name = request.form.get('part_name')
        part_number = request.form.get('part_number')
        van_number = request.form.get('van_number')
        dbm.update(part_id, part_name, part_number, van_number)
    # If the /update route is accessed, re-route to index
    return redirect(url_for('parts'))


# Route for /vans
@app.route('/vans/', methods=['GET', 'POST'])
def vans():
    dbm = DatabaseManipulator()
    van_numbers = dbm.get_van_nums()
    return render_template('vans.html', van_numbers=van_numbers)


# Route for /vans that consumes the van_id
@app.route('/vans/<van_id>/')
def van_num(van_id=0):
    dbm = DatabaseManipulator()
    results = dbm.get_vans(van_id)
    # If the results are not None, return the following
    if results is not None:
        return render_template('display_van.html', results=results)
    else:
        return redirect(url_for('vans'))


# Display the database in JSON format
@app.route('/json/', methods=['GET', 'POST'])
def get_json():
    dbm = DatabaseManipulator()
    res = make_response(jsonify(dbm.get_json()))
    return res


if __name__ == '__main__':
    app.run()

