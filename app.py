from flask import Flask, render_template, request
from src.DatabaseManipulator import DatabaseManipulator
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    dbm = DatabaseManipulator()
    results, error = dbm.fetchall()
    if request.method == 'POST':
        part_name = str(request.form['partName'])
        part_number = str(request.form['partNumber'])
        dbm.insert(part_name=part_name, part_number=part_number)
    return render_template('index.html', results=results, error=error)
