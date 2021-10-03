from os import environ

from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()


class DatabaseConnector:
    def __init__(self):
        self.host = environ.get('host')
        self.port = environ.get('webui_port')
        self.db_port = int(environ.get('db_port'))
        self.user = environ.get('username')
        self.password = environ.get('password')
        self.db = environ.get('db')
        self.conn = connect(host=self.host, user=self.user, password=self.password, database=self.db,
                            port=self.db_port)
        self.cursor = self.conn.cursor()

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_cursor(self):
        return self.cursor

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def set_conn(self, conn):
        self.conn = conn

    # Test if the connection is successful; print errors if it was not
    def get_conn(self):
        try:
            if self.conn.is_connected():
                return self.conn
        except Error as e:
            print(e)
