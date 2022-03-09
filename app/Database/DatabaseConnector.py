from os import environ


class DatabaseConnector:
    def __init__(self):
        self.host = environ.get('host')
        self.port = environ.get('webui_port')
        self.db_port = int(environ.get('db_port'))
        self.user = environ.get('username')
        self.password = environ.get('password')
        self.webui_host = environ.get('webui_host')
        self.db = environ.get('db')
