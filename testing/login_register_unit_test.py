from random import choice
from string import ascii_letters, digits
from unittest import TestCase, main
from app.Database.DatabaseManipulator import DatabaseManipulator, check_password, \
    check_password_hash, create_password_hash

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))
dbm = DatabaseManipulator()


class TestLoginRegister(TestCase):
    def test_check_password(self):
        password = 'password' + random_string
        pw_hash = create_password_hash(password.encode('utf8'))
        self.assertFalse(check_password('password' + random_digit, 'password' + random_string))
        print('check_password() False input test -> PASSED' + '\n')
        self.assertTrue(check_password_hash(password.encode('utf8'), pw_hash))
        print('check_password_hash() False input test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
