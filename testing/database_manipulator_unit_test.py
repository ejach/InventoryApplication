import unittest
from string import ascii_letters, digits
from random import choice

from app.Database.DatabaseManipulator import DatabaseManipulator, check_input

dbm = DatabaseManipulator()

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))


class DBMUnitTest(unittest.TestCase):
    # Tests the check_input function
    def test_check_input(self):
        self.assertTrue(check_input(random_string, random_numbers, random_digit))
        print('check_input() TRUE test -> PASSED' + '\n')
        self.assertFalse(check_input('', '', ''))
        print('check_input() Empty Input test -> PASSED' + '\n')
        self.assertFalse(check_input(' ', ' ', ' '))
        print('check_input() Space Input test -> PASSED' + '\n')

    def test_insert(self):
        pass

    def test_delete(self):
        pass

    def test_update(self):
        pass


if __name__ == '__main__':
    unittest.main()
