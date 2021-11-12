from time import time
from unittest import TestCase, main
from random import choice
from string import ascii_letters, digits

from app.Database.DatabaseManipulator import DatabaseManipulator, check_input, create_password_hash, check_password, \
    check_password_hash
from app.Database.TestDatabaseStatements import TestDatabaseStatements

dbm = DatabaseManipulator()
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
    return str(final_res)


# Delete account by ID using get_last_id()
def delete_account():
    get_account = tdbs.get_get_last_id()
    dbm.cursor.execute(get_account)
    account_res = dbm.cursor.fetchone()
    delete_me = tdbs.get_delete_account_by_id()
    dbm.cursor.execute(delete_me, account_res)
    dbm.conn.commit()


# Check if part exists
def check_if_part_exist(part_name, part_number, van_number):
    get_part = tdbs.get_check_part_existence()
    values = (part_name, part_number, van_number,)
    dbm.cursor.execute(get_part, values)
    results = dbm.cursor.fetchall()
    if not results:
        return False
    else:
        return True


class DBMUnitTest(TestCase):
    # Checks the different functions that interact with the parts database
    def test_parts(self):
        part_name = random_string + random_time_string
        part_number = random_numbers + random_time_string
        van_number = random_string + random_time_string
        # Add a part into the database
        dbm.insert(part_name, part_number, van_number)
        # Check if it exists
        self.assertTrue(check_if_part_exist(part_name, part_number, van_number))
        print('insert() TRUE test -> PASSED' + '\n')
        # Delete the newly added part
        dbm.delete(get_last_id())
        self.assertFalse(check_if_part_exist(part_name, part_number, van_number))
        print('delete() test -> PASSED' + '\n')
        # Add another part into the database
        dbm.insert(part_name, part_number, van_number)
        # Check that it exists, again
        self.assertTrue(check_if_part_exist(part_name, part_number, van_number))
        # Update it
        dbm.update(get_last_id(), part_name + random_digit, part_number + random_digit, van_number + random_digit)
        # Check that it exists
        self.assertTrue(check_if_part_exist(part_name + random_digit, part_number + random_digit,
                                            van_number + random_digit))
        # Delete it
        dbm.delete(get_last_id())
        # Check existence
        self.assertFalse(check_if_part_exist(part_name + random_digit, part_number + random_digit,
                                             van_number + random_digit))
        print('update() test -> PASSED' + '\n')

    # Tests the check_input function
    def test_check_input(self):
        # Assert that normal input will be entered into the database
        self.assertTrue(check_input(random_string))
        self.assertTrue(check_input(random_digit))
        self.assertTrue(check_input(random_numbers))
        print('check_input() TRUE test -> PASSED' + '\n')
        # Assert that null or empty spaces alone will not be entered into the database
        self.assertFalse(check_input(''))
        print('check_input() Empty Input test -> PASSED' + '\n')
        self.assertFalse(check_input(' '))
        print('check_input() Space Input test -> PASSED' + '\n')

    # Tests the add_van function
    def test_add_van(self):
        # Create a test_van with a random string of numbers
        van_name = 'test_van' + random_string
        # Insert it into the database
        dbm.insert_van(van_name)
        # Assert that check_if_exists will return True
        self.assertTrue(dbm.check_if_exists(van_name))
        print('insert_van() test -> PASSED' + '\n')
        # Get the lastrowid and delete it from the database
        van_id = get_last_id()
        dbm.delete_van(van_id)
        # Assert that check_if_exists will return False since it is now deleted
        self.assertFalse(dbm.check_if_exists(van_name))
        print('insert_van() FALSE test -> PASSED' + '\n')

    # Tests the delete_van function
    def test_delete_van(self):
        # Create a test_van with a random digit
        van_name = 'test_van' + random_digit
        # Insert it into the database
        dbm.insert_van(van_name)
        # Delete the van from the database after getting the lastrowid
        van_id = get_last_id()
        dbm.delete_van(van_id)
        # Check if it exists in the database after deleting
        self.assertFalse(dbm.check_if_exists(van_name))
        print('delete_van() test -> PASSED' + '\n')

    # Tests the update_van function
    def test_update_van(self):
        # Create a van with a random string
        van_name = 'test_van' + random_string
        # Van name to be updated to
        new_van_name = 'new_van_name' + random_string
        # Insert it into the database
        dbm.insert_van(van_name)
        # Get the row id after inserting
        van_id = get_last_id()
        # Update it to a new van name
        dbm.update_van(van_id, new_van_name)
        # Check if the van exists
        self.assertTrue(dbm.check_if_exists(new_van_name))
        # When finished, delete the van from the database
        dbm.delete_van(van_id)
        # Make sure this operation was successful
        self.assertFalse(dbm.check_if_exists(new_van_name))
        print('update_van() test -> PASSED' + '\n')

    # Tests the check_duplicates function
    def test_check_duplicates(self):
        # Create a van name with a string of random numbers
        van_name = 'test_van' + random_numbers
        # Insert it into the database
        dbm.insert_van(van_name)
        # Assert that check_duplicates will return false as it exists in the database
        self.assertFalse(dbm.check_duplicates(van_name))
        print('check_duplicates() duplicate van FALSE test -> PASSED' + '\n')
        # Get the lastrowid and delete it
        van_id = get_last_id()
        dbm.delete_van(van_id)
        # Since it is now deleted, check if check_duplicates will return True
        self.assertTrue(dbm.check_duplicates(van_name))
        print('check_duplicates() duplicate van TRUE test -> PASSED' + '\n')

    # Test the check_password function
    def test_check_password(self):
        # Create random password
        password = 'password' + random_string
        # Hash this password
        pw_hash = create_password_hash(password.encode('utf8'))
        # Check that the check_password fails incorrect input
        self.assertFalse(check_password('password' + random_string, random_string))
        print('check_password() False input test -> PASSED' + '\n')
        # Check that the check_password passes on correct input
        self.assertTrue(check_password_hash(password.encode('utf8'), pw_hash))
        print('check_password_hash() False input test -> PASSED' + '\n')

    # Test the register functionality
    def test_register(self):
        # Check if conf_pass will fail
        dbm.register(username=username, password=password, conf_password=random_string)
        # Check if account exists
        self.assertFalse(dbm.check_if_account_exists(username))
        print('register() FALSE test -> PASSED' + '\n')
        # Check if register will pass
        dbm.register(username=username, password=password, conf_password=password)
        # Check if it exists, assume it does
        self.assertTrue(dbm.check_if_account_exists(username))
        print('register() TRUE test -> PASSED' + '\n')
        # Delete when finished
        delete_account()
        self.assertFalse(dbm.check_if_account_exists(username))
        print('register() test -> PASSED' + '\n')

    # Test the login functionality
    def test_login(self):
        # Register test account
        dbm.register(username=username, password=password, conf_password=password)
        print('login() register test -> PASSED' + '\n')
        # Assume it passes with correct credentials
        self.assertTrue(dbm.login(username, password))
        print('login() TRUE test -> PASSED' + '\n')
        # Assume it fails with incorrect credentials
        self.assertFalse(dbm.login(username, random_string))
        print('login() FALSE test -> PASSED' + '\n')
        # Delete when finished
        delete_account()
        self.assertFalse(dbm.check_if_account_exists(username))
        print('login() test -> PASSED' + '\n')


if __name__ == '__main__':
    main()
