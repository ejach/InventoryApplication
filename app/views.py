from os import environ
from bleach import clean
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.exceptions import HTTPException, abort

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator

app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')

# Instantiate the DatabaseManipulator
dbm = DatabaseManipulator()
# Instantiate the DatabaseConnector
dbc = DatabaseConnector()


# Handle the 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', e=e)


# Handle the 500 error
@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', e=e)


# app route for /login
@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = clean(request.form.get('username'))
            password = clean(request.form.get('password'))
            my_login = dbm.login(username=username, password=password)
            if my_login:
                session['logged_in'] = True
                session['username'] = username
                return render_template('index.html')
            elif not my_login:
                return render_template('login.html')
        if 'logged_in' not in session:
            return render_template('login.html')
        else:
            return redirect(url_for('index'))
    except IndexError:
        abort(404), 404
    except HTTPException:
        abort(500)


# app route for /register
@app.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = clean(request.form.get('username'))
            password = clean(request.form.get('password'))
            conf_password = clean(request.form.get('confPassword'))
            dbm.register(username, password, conf_password)
            return redirect(url_for('login'))
        else:
            return render_template('register.html')
    except IndexError:
        abort(404), 404
    except HTTPException:
        abort(500)


# app route for /logout
@app.route('/logout', strict_slashes=False, methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', default=None)
    session.pop('username', default=None)
    return redirect(url_for('index'))


# Main index.html route
@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        try:
            username = session['username']
            return render_template('index.html', username=username)
        except IndexError:
            abort(404), 404
        except HTTPException:
            abort(500)


# parts.html route
@app.route('/parts', strict_slashes=False, methods=['GET', 'POST'])
def parts():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
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
        try:
            return render_template('parts.html', results=results, webui_host=webui_host, van_nums=van_nums)
        except IndexError:
            abort(404), 404
        except HTTPException:
            abort(500)


# Displays the table code in table.html so it can be refreshed dynamically without reloading the page
@app.route('/table/<table_name>/<van_number>', strict_slashes=False, methods=['GET', 'POST'])
def table(table_name, van_number):
    # Requirements to return the results for a van by its number
    if table_name == 'vans' and van_number != 'all':
        results = dbm.get_vans(van_number)
        check_exist = dbm.check_if_exists(van_number)
        return render_template('load/van_table.html', results=results, check_exist=check_exist)
    # Requirements to return the master list of parts
    elif table_name == 'main' and van_number == 'all':
        results = dbm.fetchall()
        van_nums = dbm.get_van_nums()
        return render_template('load/table.html', results=results, van_nums=van_nums)
    # if table_name is vans_list, and van_number is all, return the following
    elif table_name == 'vans_list' and van_number == 'all':
        van_nums = dbm.get_van_nums()
        return render_template('load/vans_list.html', van_numbers=van_nums)
    # If the url is attempted to be accessed, redirect to index
    else:
        return redirect(url_for('index'))


# Route for the delete method
@app.route('/delete/<id_type>', strict_slashes=False, methods=['POST', 'GET'])
def delete(id_type):
    # If the id_type is part, delete the part
    if request.method == 'POST' and id_type == 'part':
        part_id = request.form.get('Delete')
        dbm.delete(part_id)
    # If the id_type is a van, delete the van
    elif request.method == 'POST' and id_type == 'van':
        van_id = request.form.get('Delete')
        dbm.delete_van(van_id)
    # If the /delete route is accessed, re-route to index
    return redirect(url_for('index'))


# Route to edit table rows using the update method
@app.route('/update/<id_type>', strict_slashes=False, methods=['POST', 'GET'])
def update(id_type):
    if request.method == 'POST' and id_type == 'part':
        part_id = clean(request.form.get('id'))
        part_name = clean(request.form.get('part_name'))
        part_number = clean(request.form.get('part_number'))
        van_number = clean(request.form.get('van_number'))
        dbm.update(part_id, part_name, part_number, van_number)
    elif request.method == 'POST' and id_type == 'van':
        van_id = request.form.get('id')
        van_number = request.form.get('van_number')
        dbm.update_van(van_id, van_number)
    # If the /update route is accessed, re-route to index
    return redirect(url_for('index'))


# Route for /vans
@app.route('/vans', strict_slashes=False, methods=['GET', 'POST'])
def vans():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        van_numbers = dbm.get_van_nums()
        if request.method == 'POST':
            van_number = request.form.get('van_number')
            dbm.insert_van(van_number)
        try:
            return render_template('vans.html', van_numbers=van_numbers)
        except IndexError:
            abort(404), 404
        except HTTPException:
            abort(500)


# Route for /vans that consumes the van_id
@app.route('/vans/<van_id>', strict_slashes=False)
def van_num(van_id=0):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        results = dbm.get_vans(van_id)
        check_exist = dbm.check_if_exists(van_id)
        # If there are no results in the van database, but it exists, execute the following
        if results is None and check_exist:
            return render_template('display_van.html', results=None, check_exist=check_exist)
        # If the results are not None, return the following
        elif results is not None:
            return render_template('display_van.html', results=results)
        # Otherwise, redirect to the main /vans page
        else:
            return redirect(url_for('vans'))
