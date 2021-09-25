from os import environ
from sqlite3 import connect, Row
from dotenv import load_dotenv

load_dotenv()

host = environ.get('host')
database_file = environ.get('db_file')
database = environ.get('db')

db = connect(database_file, check_same_thread=False)
db.row_factory = Row
cursor = db.cursor()


def fetchall():
    stmt = 'SELECT * FROM parts'
    cursor.execute(stmt)
    results = cursor.fetchall()
    return results
