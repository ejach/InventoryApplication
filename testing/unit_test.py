import sqlite3
from json import loads
from os import environ
from unittest import TestCase, main
from unittest.mock import MagicMock

from dotenv import load_dotenv
from requests import get

from src.DatabaseConnector import DatabaseConnector

load_dotenv()

host = environ.get('HOST')
port = environ.get('PORT')
database_file = environ.get('db_file')
database = environ.get('db')


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
        sqlite3.connect = MagicMock(return_value='Connection Successful')
        test_db_class = DatabaseConnector
        sqlite3.connect.assert_called_with(test_db_class)
        self.assertEqual(test_db_class.get_database, 'Connection Successful')
        print('SQLite3 Connection test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
