from flask import Flask, render_template
from db_manipulator import fetchall
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    results = fetchall()
    return render_template('index.html', results=results)
