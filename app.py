from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from bleach import clean

from src.DatabaseConnector import DatabaseConnector
from src.DatabaseManipulator import DatabaseManipulator

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    dbm = DatabaseManipulator()
    dbc = DatabaseConnector()
    results = dbm.fetchall()
    host = dbc.get_host()
    port = dbc.get_port()
    webui_host = dbc.get_webui_host()
    if request.method == 'POST':
        # Sanitizes the input using escape
        part_name = clean(request.form['partName'])
        part_number = clean(request.form['partNumber'])
        # Insert into the database
        dbm.insert(part_name=part_name, part_number=part_number)
        # Redirect when finished
        return redirect(url_for('index'))
    return render_template('index.html', results=results, webui_host=host, host=host, port=port)


# Display the database in JSON format
@app.route('/json', methods=['GET', 'POST'])
def get_json():
    dbm = DatabaseManipulator()
    res = make_response(jsonify(dbm.get_json()))
    return res
