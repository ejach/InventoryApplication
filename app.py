from flask import Flask, render_template
from src.DatabaseManipulator import DatabaseManipulator
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    dbm = DatabaseManipulator()
    results = dbm.fetchall()
    return render_template('index.html', results=results)
