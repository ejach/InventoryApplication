from os import environ
from sqlite3 import connect, Row
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnector:
    def __init__(self):
        self.host = environ.get('host')
        self.database_file = environ.get('db_file')
        self.database = environ.get('db')
        self.db = connect(self.database_file, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.db.row_factory = Row
