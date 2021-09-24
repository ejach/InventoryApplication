from os import environ
from unittest import TestCase, main

from requests import get

host = environ.get('HOST')
port = environ.get('PORT')


class MyTestCase(TestCase):
    # Test the status of the WSGI web server
    def test_connection(self):
        r = get(f'http://{host}:{port}')
        self.assertTrue(r.status_code == 200)
        print('HTTP 200 test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
