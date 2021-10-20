from bleach import clean
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify

from src.DatabaseConnector import DatabaseConnector
from src.DatabaseManipulator import DatabaseManipulator

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    dbm = DatabaseManipulator()
    dbc = DatabaseConnector()
    results = dbm.fetchall()
    webui_host = dbc.get_webui_host()
    van_nums = dbm.get_van_nums()
    if request.method == 'POST':
        # Sanitizes the input using escape
        part_name = clean(request.form['partName'])
        part_number = clean(request.form['partNumber'])
        van_number = request.form['van']
        # Insert into the database
        dbm.insert(part_name=part_name, part_number=part_number, van_number=van_number)
        # Redirect when finished
        return redirect(url_for('index'))
    return render_template('index.html', results=results, webui_host=webui_host, van_nums=van_nums)


# Displays the table code in table.html so it can be refreshed dynamically without reloading the page
@app.route('/table', methods=['GET', 'POST'])
def table():
    dbm = DatabaseManipulator()
    results = dbm.fetchall()
    return render_template('table.html', results=results)


# Route for the delete method
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    dbm = DatabaseManipulator()
    if request.method == 'POST':
        part_id = request.form.get('Delete')
        dbm.delete(part_id)
    # If the /delete route is accessed, re-route to index
    return redirect(url_for('index'))


# Route to edit table rows using the update method
@app.route('/update', methods=['POST', 'GET'])
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
@app.route('/vans', methods=['GET', 'POST'])
def vans():
    dbm = DatabaseManipulator()
    van_numbers = dbm.get_van_nums()
    return render_template('vans.html', van_numbers=van_numbers)


# Display the database in JSON format
@app.route('/json', methods=['GET', 'POST'])
def get_json():
    dbm = DatabaseManipulator()
    res = make_response(jsonify(dbm.get_json()))
    return res
