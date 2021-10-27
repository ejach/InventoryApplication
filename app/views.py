from bleach import clean
from flask import Flask, render_template, request, redirect, url_for

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator

app = Flask(__name__)


# Main index.html route
@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def index():
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
@app.route('/table/<table_name>/<van_number>', strict_slashes=False, methods=['GET', 'POST'])
def table(table_name, van_number):
    dbm = DatabaseManipulator()
    # Requirements to return the results for a van by its number
    if table_name == 'vans' and van_number != 'all':
        results = dbm.get_vans(van_number)
        return render_template('load/van_table.html', results=results)
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
@app.route('/delete', strict_slashes=False, methods=['POST', 'GET'])
def delete():
    dbm = DatabaseManipulator()
    if request.method == 'POST':
        part_id = request.form.get('Delete')
        dbm.delete(part_id)
    # If the /delete route is accessed, re-route to index
    return redirect(url_for('index'))


# Route to edit table rows using the update method
@app.route('/update', strict_slashes=False, methods=['POST', 'GET'])
def update():
    dbm = DatabaseManipulator()
    if request.method == 'POST':
        part_id = request.form.get('id')
        part_name = request.form.get('part_name')
        part_number = request.form.get('part_number')
        van_number = request.form.get('van_number')
        dbm.update(part_id, part_name, part_number, van_number)
    # If the /update route is accessed, re-route to index
    return redirect(url_for('index'))


# Route for /vans
@app.route('/vans', strict_slashes=False, methods=['GET', 'POST'])
def vans():
    dbm = DatabaseManipulator()
    van_numbers = dbm.get_van_nums()
    if request.method == 'POST':
        van_number = request.form.get('van_number')
        dbm.insert_van(van_number)
    return render_template('vans.html', van_numbers=van_numbers)


# Route for /vans that consumes the van_id
@app.route('/vans/<van_id>', strict_slashes=False)
def van_num(van_id=0):
    dbm = DatabaseManipulator()
    results = dbm.get_vans(van_id)
    # If the results are not None, return the following
    if results is not None:
        return render_template('display_van.html', results=results)
    else:
        return redirect(url_for('vans'))
