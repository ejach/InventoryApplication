import sqlite3
from json import loads
from os import path
from unittest import TestCase, main
from unittest.mock import MagicMock

from dotenv import load_dotenv
from requests import get

from src.DatabaseConnector import DatabaseConnector

load_dotenv()

dbc = DatabaseConnector()

host = dbc.get_host()
port = dbc.get_port()
database_file = dbc.get_database_file()
database = dbc.get_database()


def is_json(my_json):
    try:
        loads(my_json)
    except ValueError as e:
        print(e)
        return False
    return True


class TestApplication(TestCase):
    def setUp(self) -> None:
        print('****SETUP****')
        pass

    def tearDown(self) -> None:
        print('****TEARDOWN****')
        pass

    # Test the status of the WSGI web server
    def test_connection(self):
        r = get(f'http://{host}:{port}')
        self.assertTrue(r.status_code == 200)
        print('HTTP 200 test -> PASSED' + '\n')

    def test_sqlite_conn(self):
        self.assertTrue(path.exists(f'../{database_file}'))
        print('SQLite3 file exists -> PASSED' + '\n')
        sqlite3.connect = MagicMock(return_value='Connection is Successful')
        tdbc = TestDatabaseClass()
        sqlite3.connect.assert_called_with('database.db')
        self.assertEqual(tdbc.connection, 'Connection is Successful')
        print('SQLite3 test -> PASSED' + '\n')


class TestDatabaseClass:

    def __init__(self, connection_string='database.db'):
        self.connection = sqlite3.connect(connection_string)


if __name__ == '__main__':
    main()
# TODO create tests that validate MySQL connection, and creates a test database that verifies the statements
