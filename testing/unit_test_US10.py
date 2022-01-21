from random import choice
from string import ascii_letters, digits
from time import time
from unittest import TestCase, main
from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator
from app.Database.TestDatabaseStatements import TestDatabaseStatements

dbm = DatabaseManipulator()
dbc = DatabaseConnector()
tdbs = TestDatabaseStatements()

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))

# Gets the epoch time and truncates the trailing decimals
random_time_string = str(int(time()))

username = 'user' + random_time_string
password = 'pass' + random_time_string


# Get last id of entry that was inserted into the database
def get_last_id():
    get_id = tdbs.get_get_last_id()
    dbm.cursor.execute(get_id)
    id_res = dbm.cursor.fetchone()
    final_res = (','.join(str(a) for a in id_res))
    print(final_res)
    return str(final_res)


class UnitTest(TestCase):

    def test_login_confirmation(self):
        # Register new account
        dbm.register(username=username, password=password, conf_password=password)
        last_id = dbm.cursor.lastrowid
        self.assertTrue(dbm.check_if_account_exists(username=username))
        print('CREATE ACCOUNT TEST -> PASSED')
        # Check login with this account, expected output is false
        self.assertFalse(dbm.login(username=username, password=password))
        print('LOGIN ACCOUNT UNCONFIRMED TEST -> PASSED')
        # Confirm account
        dbm.confirm_account(last_id)
        # Login to newly confirmed account
        self.assertTrue(dbm.login(username, password))
        print('LOGIN ACCOUNT CONFIRMED TEST -> PASSED')
        # Delete account afterwards
        dbm.delete_account(last_id)
        # Make sure it does not exist anymore
        self.assertFalse(dbm.check_if_account_exists(username))
        print('DELETE ACCOUNT TEST -> PASSED')


if __name__ == '__main__':
    main()
