from src.DatabaseConnector import DatabaseConnector
from src.DatabaseManipulator import DatabaseManipulator
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    dbm = DatabaseManipulator()
    dbc = DatabaseConnector()
    results = dbm.fetchall()
    host = dbc.get_host()
    port = dbc.get_port()
    if request.method == 'POST':
        part_name = request.form['partName']
        part_number = request.form['partNumber']
        dbm.insert(part_name=part_name, part_number=part_number)
        return redirect(url_for('index'))
    return render_template('index.html', results=results, host=host, port=port)
