from os import environ
from sqlite3 import connect, Row
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnector:
    def __init__(self):
        self.host = environ.get('host')
        self.port = environ.get('port')
        self.database_file = environ.get('db_file')
        self.database = connect(self.database_file, check_same_thread=False)
        self.cursor = self.database.cursor()
        self.database.row_factory = Row

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def set_database_file(self, database_file):
        self.database_file = database_file

    def get_database_file(self):
        return self.database_file

    def set_database(self, database):
        self.database = database

    def get_database(self):
        return self.database

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_cursor(self):
        return self.cursor
