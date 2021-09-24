from unittest import TestCase, main

from requests import get


class MyTestCase(TestCase):
    # Test the status of the WSGI web server
    def test_connection(self):
        r = get('http://localhost:8000')
        self.assertTrue(r.status_code == 200)
        print('HTTP 200 test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
