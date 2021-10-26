from unittest import TestCase, main

from requests import get, post
from responses import GET, activate, add, POST

from app.Database.DatabaseConnector import DatabaseConnector

dbc = DatabaseConnector()
host = dbc.get_host()
port = dbc.get_port()


class TestApplication(TestCase):
    def setUp(self) -> None:
        print('****SETUP****')
        pass

    def tearDown(self) -> None:
        print('****TEARDOWN****')
        pass

    # Test the status of the WSGI web server
    def test_connection(self):
        r = get(f'http://localhost:5000')
        self.assertTrue(r.status_code == 200)
        print('HTTP 200 test -> PASSED' + '\n')
        pass

    def test_mysql_conn(self):
        self.assertTrue(dbc.conn.is_connected())

    @activate
    def testHTTP404(self):
        add(**{
            'method': GET,
            'url': f'http://{host}:{port}',
            'body': '{"error": "reason"}',
            'status': 404,
            'content_type': 'application/json',
            'adding_headers': {'X-Foo': 'Bar'}
        })
        response = get(f'http://{host}:{port}')
        self.assertEqual({'error': 'reason'}, response.json())
        print('HTTP 404 POST Request test -> PASSED' + '\n')
        self.assertEqual(404, response.status_code)
        print('HTTP 404 GET test -> PASSED' + '\n')

    @activate
    def testPOST(self):
        add(**{
            'method': POST,
            'url': f'http://{host}:{port}',
            'body': '{"error": "reason"}',
            'status': 404,
            'content_type': 'application/json',
            'adding_headers': {'X-Foo': 'Bar'}
        })
        response = post(f'http://{host}:{port}')
        self.assertEqual({'error': 'reason'}, response.json())
        print('HTTP 404 POST Request test -> PASSED' + '\n')
        self.assertEqual(404, response.status_code)
        print('HTTP 404 POST test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
# TODO create tests that validate MySQL connection, and creates a test database that verifies the statements
