from random import choice
from string import ascii_letters, digits
from time import time
from unittest import TestCase, main

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator, check_input, create_password_hash, check_password, \
    check_password_hash
from app.Database.TestDatabaseStatements import TestDatabaseStatements

# Instantiate the database classes
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


# Delete account by ID
def delete_account(this_id):
    dbm.conn.ping()
    stmt = tdbs.get_delete_account_by_id()
    dbm.cursor.execute(stmt, this_id)
    dbm.conn.close()


# Delete job by ID
def delete_job(this_id):
    dbm.conn.ping()
    stmt = tdbs.get_delete_job_by_id()
    dbm.cursor.execute(stmt, this_id)
    dbm.conn.close()


# Check if part exists
def check_if_part_exist(part_name, part_amount, part_number, van_number):
    dbm.conn.ping()
    get_part = tdbs.get_check_part_existence()
    values = (part_name, part_amount, part_number, van_number,)
    dbm.cursor.execute(get_part, values)
    results = dbm.cursor.fetchall()
    dbm.conn.close()
    if not results:
        return False
    else:
        return True


# Check if job exists
def check_if_job_exists(_username, _time, van_number, parts_used):
    dbm.conn.ping()
    stmt = tdbs.get_check_job_existence()
    values = (_username, _time, van_number, parts_used)
    dbm.cursor.execute(stmt, values)
    results = dbm.cursor.fetchall()
    dbm.conn.close()
    if not results:
        return False
    else:
        return True


# Check if van exists
def check_if_van_exist(this_id):
    dbm.conn.ping()
    get_van = tdbs.get_check_van_existence()
    dbm.cursor.execute(get_van, this_id)
    results = dbm.cursor.fetchall()
    dbm.conn.close()
    if not results:
        return False
    else:
        return True


# Get a random existing van number
def get_random_van():
    dbm.conn.ping()
    get_first_van = tdbs.get_get_random_van()
    dbm.cursor.execute(get_first_van)
    results = dbm.cursor.fetchone()
    dbm.conn.close()
    return results[0]


# Get a random existing username
def get_random_username():
    dbm.conn.ping()
    stmt = tdbs.get_get_random_username()
    dbm.cursor.execute(stmt)
    results = dbm.cursor.fetchone()
    dbm.conn.close()
    return results[0]


class DBMUnitTest(TestCase):
    # Make sure the database connection is pinged and closed after each test
    def setUp(self) -> None:
        print('***SETUP***')
        dbc.conn.ping()

    def tearDown(self) -> None:
        print('***TEARDOWN***')
        dbc.conn.close()

    # Checks the different functions that interact with the parts database
    def test_parts_delete(self):
        print('test_parts_delete() TEST')
        part_name = random_string + random_time_string
        part_number = random_numbers + random_time_string
        van_number = random_string + random_time_string
        # Create a van in the database
        dbm.insert_van(van_number)
        van_id = dbm.cursor.lastrowid
        # Make sure it exists
        self.assertTrue(dbm.check_if_exists(van_number))
        # Add a part into the database
        dbm.insert(part_name=part_name, part_number=part_number, part_amount=random_digit, van_number=van_number)
        # Check if it exists
        self.assertTrue(check_if_part_exist(part_name=part_name, part_number=part_number, part_amount=random_digit,
                                            van_number=van_number))
        print('insert() TRUE test -> PASSED')
        # Delete the newly added part by deleting the van
        dbm.delete_van(van_id)
        # Make sure the corresponding van and part do not exist
        self.assertFalse(check_if_part_exist(part_name=part_name, part_number=part_number,
                                             part_amount=random_digit, van_number=van_number))
        self.assertFalse(check_if_van_exist(van_id))
        print('delete() test -> PASSED')

    def test_parts_update(self):
        print('test_parts_update() TEST')
        # Create another van
        dbm.insert_van(random_time_string)
        van_id = dbm.cursor.lastrowid
        # Add another part into the database
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   van_number=random_time_string)
        # Get last part ID from the initial insert statement
        update_part_id = dbm.cursor.lastrowid
        # Check that it exists, again
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=random_time_string))
        # Update it
        dbm.update(update_part_id, part_name=random_string + random_string, part_number=random_numbers + random_numbers,
                   van_number=random_time_string, part_amount=random_digit + random_digit)
        # Check that it exists
        self.assertTrue(
            check_if_part_exist(part_name=random_string + random_string, part_number=random_numbers + random_numbers,
                                van_number=random_time_string, part_amount=random_digit + random_digit))
        # Delete it
        dbm.delete_van(van_id)
        # Check existence
        self.assertFalse(
            check_if_part_exist(part_name=random_string + random_digit, part_number=random_numbers + random_digit,
                                van_number=random_time_string + random_digit, part_amount=random_digit + random_digit))
        self.assertFalse(check_if_van_exist(van_id))
        print('update() test -> PASSED')

    # Tests the check_input function
    def test_check_input(self):
        print('test_check_input() TEST')
        # Assert that normal input will be entered into the database
        self.assertTrue(check_input(random_string))
        self.assertTrue(check_input(random_digit))
        self.assertTrue(check_input(random_numbers))
        print('check_input() TRUE test -> PASSED')
        # Assert that null or empty spaces alone will not be entered into the database
        self.assertFalse(check_input(''))
        print('check_input() Empty Input test -> PASSED')
        self.assertFalse(check_input(' '))
        print('check_input() Space Input test -> PASSED')

    # Tests the add_van function
    def test_add_van(self):
        print('test_add_van() TEST')
        # Create a test_van with a random string of numbers
        van_name = 'test_van' + random_string
        # Insert it into the database
        dbm.insert_van(van_name)
        van_id = dbm.cursor.lastrowid
        # Assert that check_if_exists will return True
        self.assertTrue(dbm.check_if_exists(van_name))
        print('insert_van() test -> PASSED')
        # Get the lastrowid and delete it from the database
        dbm.delete_van(van_id)
        # Assert that check_if_exists will return False since it is now deleted
        self.assertFalse(dbm.check_if_exists(van_name))
        print('insert_van() FALSE test -> PASSED')

    # Tests the delete_van function
    def test_delete_van(self):
        print('test_delete_van() TEST')
        # Create a test_van with a random digit
        van_name = 'test_van' + random_digit
        # Insert it into the database
        dbm.insert_van(van_name)
        # Get the van_id from the last insert statement
        van_id = dbm.cursor.lastrowid
        # Delete the van from the database after getting the lastrowid
        dbm.delete_van(van_id)
        # Check if it exists in the database after deleting
        self.assertFalse(dbm.check_if_exists(van_name))
        print('delete_van() test -> PASSED')

    # Tests the update_van function
    def test_update_van(self):
        print('test_update_van() TEST')
        # Create a van with a random string
        van_name = 'test_van' + random_string
        # Van name to be updated to
        new_van_name = 'new_van_name' + random_string
        # Insert it into the database
        dbm.insert_van(van_name)
        # Get the row id after inserting
        van_id = dbm.cursor.lastrowid
        # Update it to a new van name
        dbm.update_van(van_id, new_van_name)
        # Check if the van exists
        self.assertTrue(dbm.check_if_exists(new_van_name))
        # Make sure if the van name is Blank, a TypeError is raised
        dbm.update_van(van_id, '')
        self.assertRaises(TypeError)
        print('update_van() TypeError test -> PASSED')
        # When finished, delete the van from the database
        dbm.delete_van(van_id)
        # Make sure this operation was successful
        self.assertFalse(dbm.check_if_exists(new_van_name))
        print('update_van() test -> PASSED')

    # Tests the check_duplicates function
    def test_check_duplicates(self):
        print('test_check_duplicates() TEST')
        # Create a van name with a string of random numbers
        van_name = 'test_van' + random_numbers
        # Insert it into the database
        dbm.insert_van(van_name)
        # Get the lastrowid and delete it
        van_id = dbm.cursor.lastrowid
        # Assert that check_duplicates will return false as it exists in the database
        self.assertFalse(dbm.check_duplicates(van_name))
        print('check_duplicates() duplicate van FALSE test -> PASSED')
        dbm.delete_van(van_id)
        # Since it is now deleted, check if check_duplicates will return True
        self.assertTrue(dbm.check_duplicates(van_name))
        print('check_duplicates() duplicate van TRUE test -> PASSED')

    # Test the check_password function
    def test_check_password(self):
        print('test_check_password() TEST')
        # Create random password
        this_pass = 'password' + random_string
        # Hash this password
        pw_hash = create_password_hash(this_pass.encode('utf8'))
        # Check that the check_password fails incorrect input
        self.assertFalse(check_password('password' + random_string, random_string))
        print('check_password() False input test -> PASSED')
        # Check that the check_password passes on correct input
        self.assertTrue(check_password_hash(this_pass.encode('utf8'), pw_hash))
        print('check_password_hash() False input test -> PASSED')

    # Test the confirmation database attribute of the account functionality
    def test_login_confirmation(self):
        print('test_login_confirmation() TEST')
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

    # Test that the deny/delete functionality works
    def test_login_deny(self):
        print('test_login_deny() TEST')
        # Create an account
        dbm.register(username, password, password)
        # Get account id
        acc_id = dbm.cursor.lastrowid
        # Make sure account exists
        self.assertTrue(dbm.check_if_account_exists(username))
        print('CREATE DENIED ACCOUNT TEST -> PASSED')
        # Deny the account
        dbm.delete_account(acc_id)
        # Make sure the account doesn't exist anymore
        self.assertFalse(dbm.check_if_account_exists(username))
        print('DELETE DENIED ACCOUNT TEST -> PASSED')
        # Make sure you cannot login anymore with this account
        self.assertFalse(dbm.login(username, password))
        print('FAIL LOGIN ACCOUNT TEST -> PASSED')

    # Test the adding of part amounts attribute into the database
    def test_add_part_amount(self):
        print('test_add_part_amount() TEST')
        # Create test van
        dbm.insert_van(random_time_string)
        # Get the van ID
        van_id = dbm.cursor.lastrowid
        # Make sure it exists
        self.assertTrue(check_if_van_exist(van_id))
        # Insert a random part into the database with random values
        dbm.insert(random_string, random_digit, random_digit, random_time_string)
        # Make sure it was inserted into the database
        self.assertTrue(check_if_part_exist(random_string, random_digit, random_digit, random_time_string))
        print('insert() part amount TRUE test -> PASSED')
        # Delete the van and the part that it contains when finished
        dbm.delete_van(van_id)
        # Make sure it was deleted
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_numbers,
                                             part_number=random_digit, van_number=random_time_string))
        self.assertFalse(check_if_van_exist(van_id))
        print('insert() part amount FALSE test -> PASSED')

    # Test invalid input in the part amount attribute column
    def test_false_part_amount(self):
        print('test_false_part_amount() TEST')
        # Insert a part into the database with invalid part values (string where it is expecting an int)
        dbm.insert(part_name=random_string, part_amount=random_string, part_number=random_digit,
                   van_number=random_digit)
        # Make sure it was rejected from the database
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_numbers,
                                             part_number=random_digit, van_number=random_digit))
        print('insert() part amount invalid input test -> PASSED')

    # Test updating the part amount into the database
    def test_update_part_amount(self):
        print('test_update_part_amount() TEST')
        # Insert van number into database
        dbm.insert_van(random_time_string)
        # Get van ID
        van_id = dbm.cursor.lastrowid
        # Check if it exists
        self.assertTrue(dbm.check_if_exists(random_time_string))
        # Insert a random part into the database
        dbm.insert(part_name=random_string, part_amount=random_digit + random_digit, part_number=random_digit,
                   van_number=random_time_string)
        # Get the ID of the last inserted part
        part_id = dbm.cursor.lastrowid
        # Make sure it exists
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_digit + random_digit,
                                            part_number=random_digit, van_number=random_time_string))
        print('insert() part amount update insert test -> PASSED')
        # Update the part with random values
        dbm.update(part_id, part_name=random_string, part_amount=random_time_string, part_number=random_digit,
                   van_number=random_time_string)
        # Make sure the part exists based on these random values
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_time_string,
                                            part_number=random_digit, van_number=random_time_string))
        print('insert() part amount update test -> PASSED')
        # Delete the van and the part that it contains when finished
        dbm.delete_van(van_id)
        # Make sure the part and van was actually deleted
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_time_string,
                                             part_number=random_digit, van_number=random_time_string))
        self.assertFalse(check_if_van_exist(van_id))

    # Test the toggling of accounts to have admin privileges in the is_admin attribute
    def test_toggle_admin(self):
        print('test_toggle_admin() TEST')
        # Register a random user account
        dbm.register(username=username, password=password, conf_password=password)
        this_id = dbm.cursor.lastrowid
        self.assertTrue(dbm.check_if_account_exists(username))
        # Make the specified account an admin
        dbm.modify_admin(this_id, 1)
        self.assertEqual(dbm.check_admin(username), 1)
        print('MAKE ADMIN TEST -> PASSED')
        # Remove admin privileges from the account
        dbm.modify_admin(this_id, 0)
        self.assertEqual(dbm.check_admin(username), 0)
        print('REMOVE ADMIN TEST -> PASSED')
        # Delete the account when finished
        dbm.delete_account(this_id)
        self.assertFalse(dbm.check_if_account_exists(username))
        print('REMOVE ACCOUNT TEST -> PASSED')

    # Test the get_selections() method
    def test_get_selections(self):
        print('test_get_selections() TEST')
        # Create random string
        this_string = random_digit + random_digit + random_time_string
        # Insert random van into database
        dbm.insert_van(this_string)
        this_id = dbm.cursor.lastrowid
        # Make sure the method returns the string that was inserted
        self.assertIn(member=(this_string, this_string), container=dbm.get_selections())
        print('get_selections TEST -> PASSED')
        # Delete when finished
        dbm.delete_van(this_id)
        # Make sure the van has been deleted
        self.assertFalse(check_if_van_exist(this_id))
        print('check_if_van_exist() TEST -> PASSED')

    # Check the updating of the van on a part in the update function
    def test_update_parts_van(self):
        print('test_update_parts() TEST')
        # Create a new van
        dbm.insert_van(random_time_string)
        van_id = dbm.cursor.lastrowid
        # Get random van from existing vans
        random_van = get_random_van()
        # Get the first van
        self.assertTrue(dbm.check_if_exists(random_time_string))
        print('insert_van TEST -> PASSED')
        # Add part to new van
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   van_number=random_time_string)
        part_id = dbm.cursor.lastrowid
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=random_time_string))
        # Update the part with a random van that already exists
        dbm.update(part_id, part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   van_number=random_van)
        # Check if the part exists with the existing van
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=random_van))
        # Update the part to be back in its original van
        dbm.update(part_id, part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   van_number=random_time_string)
        # Make sure it exists
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=random_time_string))
        print('update TEST -> PASSED')
        # Delete the van and it's containing part
        dbm.delete_van(van_id)
        # Make sure neither exist
        self.assertFalse(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=random_time_string))
        self.assertFalse(check_if_van_exist(van_id))
        print('test_update_parts() TEST -> PASSED')

    def test_create_job(self):
        print('test_create_job() TEST')
        van_num = random_time_string
        # Create a random van
        dbm.insert_van(van_num)
        van_id = dbm.cursor.lastrowid
        # Make sure that you cannot create a job from a van with no parts
        dbm.record_job(random_string, random_time_string + random_digit, van_num, random_numbers)
        self.assertFalse(check_if_job_exists(random_string, random_time_string + random_digit,
                                             van_num, random_numbers))
        print('create job FALSE TEST -> PASSED')
        # Insert part, check if it exists
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   van_number=van_num)
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=random_time_string))
        # Create job, make sure it exists
        dbm.record_job(username=random_string, time=random_time_string, van_number=van_num, parts_used=random_digit)
        self.assertTrue(check_if_job_exists(_username=random_string, _time=random_time_string,
                                            van_number=van_num, parts_used=random_digit))
        print('create job TRUE TEST -> PASSED')
        # Delete the van when finished
        dbm.delete_van(van_id)
        self.assertFalse(check_if_job_exists(random_string, random_time_string + random_digit,
                                             van_num, random_numbers))
        self.assertFalse(check_if_van_exist(van_id))
        print('test_create_job() TEST -> PASSED')

    # Test if the part difference is zero to not let the job enter the database
    def test_job_part_difference(self):
        print('test_job_part_difference() TEST')
        # Insert van into database
        van_num = random_numbers
        dbm.insert_van(van_num)
        van_id = dbm.cursor.lastrowid
        self.assertTrue(check_if_van_exist(van_id))
        # Insert part into database
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   van_number=van_num)
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                van_number=van_num))
        # Make sure a job will not be recorded if the parts used is 0
        dbm.record_job(random_string, random_time_string + random_digit, van_num, parts_used=0)
        self.assertFalse(check_if_job_exists(_username=random_string, _time=random_time_string,
                                             van_number=van_num, parts_used=0))
        print('record_job FALSE TEST -> PASSED')
        dbm.record_job(random_string, random_time_string + random_digit, van_num, parts_used=random_digit)
        self.assertTrue(check_if_job_exists(_username=random_string, _time=random_time_string + random_digit,
                                            van_number=van_num, parts_used=random_digit))
        print('record_job TRUE TEST -> PASSED')
        # Delete the van when finished
        dbm.delete_van(van_id)
        self.assertFalse(check_if_job_exists(_username=random_string, _time=random_time_string + random_digit,
                                             van_number=van_num, parts_used=random_digit))
        self.assertFalse(check_if_van_exist(van_id))
        print('test_job_part_difference() TEST -> PASSED')


if __name__ == '__main__':
    main()
