from contextlib import contextmanager
from os import environ

from pymysql import connect


class DatabaseConnector:
    def __init__(self):
        self.host = environ.get('host')
        self.port = environ.get('webui_port')
        self.db_port = int(environ.get('db_port'))
        self.user = environ.get('username')
        self.password = environ.get('password')
        self.webui_host = environ.get('webui_host')
        self.db = environ.get('db')

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_password(self):
        return self.password

    def get_webui_host(self):
        return self.webui_host

    def get_db(self):
        return self.db

    @contextmanager
    def get_conn(self):
        connection = connect(host=self.host, user=self.user, password=self.password, database=self.db,
                             port=self.db_port, autocommit=True)
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            connection.close()
