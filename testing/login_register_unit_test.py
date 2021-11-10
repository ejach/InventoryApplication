from random import choice
from string import ascii_letters, digits
from unittest import TestCase, main
from app.Database.DatabaseManipulator import DatabaseManipulator, check_password, \
    check_password_hash, create_password_hash
from app.Database.TestDatabaseStatements import TestDatabaseStatements

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))

dbm = DatabaseManipulator()
tdbs = TestDatabaseStatements()


# Get id by username, delete by ID
def delete_account(username):
    get_account = tdbs.get_get_id_by_username()
    values = (username,)
    dbm.cursor.execute(get_account, values)
    account_res = dbm.cursor.fetchone()
    delete_me = tdbs.get_delete_account_by_id()
    dbm.cursor.execute(delete_me, account_res)
    dbm.conn.commit()


class TestLoginRegister(TestCase):
    # Test the check_password function
    def test_check_password(self):
        # Create random password
        password = 'password' + random_string
        # Hash this password
        pw_hash = create_password_hash(password.encode('utf8'))
        # Check that the check_password fails incorrect input
        self.assertFalse(check_password('password' + random_digit, 'password' + random_string))
        print('check_password() False input test -> PASSED' + '\n')
        # Check that the check_password passes on correct input
        self.assertTrue(check_password_hash(password.encode('utf8'), pw_hash))
        print('check_password_hash() False input test -> PASSED' + '\n')

    # Test the register functionality
    def test_register(self):
        username = 'user' + random_string
        password = 'pass' + random_string
        # Check if conf_pass will fail
        dbm.register(username=username, password=password, conf_password=random_numbers)
        # Check if account exists
        self.assertFalse(dbm.check_if_account_exists(username))
        print('register() FALSE test -> PASSED' + '\n')
        # Check if register will pass
        dbm.register(username=username, password=password, conf_password=password)
        # Check if it exists, assume it does
        self.assertTrue(dbm.check_if_account_exists(username))
        print('register() TRUE test -> PASSED' + '\n')
        # Delete when finished
        delete_account(username)
        self.assertFalse(dbm.check_if_account_exists(username))
        print('register() test -> PASSED' + '\n')

    # Test the login functionality
    def test_login(self):
        username = 'user' + random_string
        password = 'pass' + random_string
        # Register test account
        dbm.register(username=username, password=password, conf_password=password)
        print('login() register test -> PASSED' + '\n')
        # Assume it passes with correct credentials
        self.assertTrue(dbm.login(username, password))
        print('login() TRUE test -> PASSED' + '\n')
        # Assume it fails with incorrect credentials
        self.assertFalse(dbm.login(username, random_numbers))
        print('login() FALSE test -> PASSED' + '\n')
        # Delete when finished
        delete_account(username)
        self.assertFalse(dbm.check_if_account_exists(username))
        print('login() test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
