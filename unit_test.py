import sqlite3
from os import environ
from unittest import TestCase, main
from unittest.mock import MagicMock

from requests import get
from dotenv import load_dotenv

load_dotenv()

host = environ.get('HOST')
port = environ.get('PORT')
database_file = environ.get('db_file')
database = environ.get('db')


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
        test_db_class = TestDatabaseClass()
        sqlite3.connect.assert_called_with(database)
        self.assertEqual(test_db_class.connection, 'Connection Successful')
        print('SQLite3 Connection test -> PASSED' + '\n')


class TestDatabaseClass:
    def __init__(self, database_conn=database):
        self.connection = sqlite3.connect(database_conn)


if __name__ == '__main__':
    main()
