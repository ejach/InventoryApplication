from os import environ

from pymysql import connect, Error


class DatabaseConnector:
    def __init__(self):
        self.host = environ.get('host')
        self.port = environ.get('webui_port')
        self.db_port = int(environ.get('db_port'))
        self.user = environ.get('username')
        self.password = environ.get('password')
        self.webui_host = environ.get('webui_host')
        self.db = environ.get('db')
        self.conn = connect(host=self.host, user=self.user, password=self.password, database=self.db,
                            port=self.db_port, autocommit=True)
        self.cursor = self.conn.cursor()

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_cursor(self):
        return self.cursor

    def get_password(self):
        return self.password

    def get_webui_host(self):
        return self.webui_host

    def get_db(self):
        return self.db

    # Test if the connection is successful; print errors if it was not
    def get_conn(self):
        try:
            if self.conn.open:
                return self.conn
        except Error as e:
            print(e)
        finally:
            self.conn.close()
