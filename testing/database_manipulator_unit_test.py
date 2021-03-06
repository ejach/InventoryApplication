from os import getenv, listdir
from random import choice, randint
from string import ascii_letters, digits
from time import time
from unittest import TestCase, main

from sqlalchemy import select, func
from sqlalchemy.sql.functions import count

from app.Database.DatabaseManipulator import DatabaseManipulator, check_input, create_password_hash, check_password, \
    check_password_hash, check_phone_num, get_current_store_name_icon
from app.Database.DatabaseTables import PartStore, Part, Account, Job, PartType
from app.decorators import DatabaseSession
from app.decorators.flask_decorators import db_connector

# Instantiate the database classes
dbm = DatabaseManipulator()
session = DatabaseSession()

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))

# Gets the epoch time and truncates the trailing decimals
random_time_string = str(int(time()))

username = 'user' + random_time_string
password = 'pass' + random_time_string


# Generate random phone number
def random_phone_num_generator():
    first = str(randint(100, 999))
    second = str(randint(1, 888)).zfill(3)
    last = (str(randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(randint(1, 9998)).zfill(4))
    return '1{}{}{}'.format(first, second, last)


# Get random icon from list
def get_random_icon():
    items = listdir('../app/static/assets/stores/')
    return choice([i.rstrip('.svg') for i in items])


# Check if part exists
@db_connector
def check_if_part_exist(part_name, part_amount, part_number, part_store_name, part_type, **kwargs):
    connection = kwargs.pop('connection')
    get_part = (select(Part.name, Part.amount, Part.part_number, PartStore.part_store_name)
                .where(Part.name == part_name, Part.amount == part_amount, Part.part_number == part_number,
                       Part.part_store_name == part_store_name, Part.type == part_type))
    results = connection.execute(get_part).fetchall()
    if not results:
        return False
    else:
        return True


# Check if job exists
@db_connector
def check_if_job_exists(_username, _time, part_store, parts_used, **kwargs):
    connection = kwargs.pop('connection')
    stmt = (select(Job.username, Job.time, Job.part_store_name, Job.parts_used)
            .where(Job.username == _username, Job.time == _time, Job.part_store_name == part_store,
                   Job.parts_used == parts_used))
    results = connection.execute(stmt).fetchall()
    if not results:
        return False
    else:
        return True


# Get max ID from low_parts
@db_connector
def get_low_part_id(**kwargs):
    connection = kwargs.pop('connection')
    stmt = (select(func.max(Part.id)).where(Part.low_thresh > Part.amount))
    results = connection.execute(stmt).fetchall()
    return results[0][0]


# Check if part_store exists
@db_connector
def check_if_part_store_exists(this_id, **kwargs):
    connection = kwargs.pop('connection')
    get_part_store = (select(PartStore.id, PartStore.part_store_name).where(PartStore.id == this_id))
    results = connection.execute(get_part_store).fetchall()
    if not results:
        return False
    else:
        return True


# Check if part_store exists by name
@db_connector
def check_part_store_name(part_store_name, **kwargs):
    connection = kwargs.pop('connection')
    get_part_store = (select(PartStore.id, PartStore.part_store_name)
                      .where(PartStore.part_store_name == part_store_name))
    results = connection.execute(get_part_store).fetchall()
    if not results:
        return False
    else:
        return True


# Check if part type exists
@db_connector
def check_if_type_exist(this_id, **kwargs):
    connection = kwargs.pop('connection')
    get_part_type = (select(PartType.id, PartType.type_name).where(PartType.id == this_id))
    results = connection.execute(get_part_type).fetchall()
    if not results:
        return False
    else:
        return True


# Get the last ID inserted into the database by Table Object passed in
@db_connector
def get_last_id(*args, **kwargs):
    connection = kwargs.pop('connection')
    for arg in args:
        get_id = (select(func.max(arg.id)))
        results = connection.execute(get_id).fetchone()
        return results


# Get a random existing partStore number
@db_connector
def get_random_part_store(**kwargs):
    connection = kwargs.pop('connection')
    get_first_part_store = (select(PartStore.part_store_name).order_by(func.rand()).limit(1))
    results = connection.execute(get_first_part_store).fetchone()
    return results[0]


# Get part type duplicates
@db_connector
def get_part_type_duplicates(type_name, **kwargs):
    connection = kwargs.pop('connection')
    stmt = (select(count(PartType.type_name)).where(PartType.type_name == type_name))
    results = connection.execute(stmt).fetchone()
    return results


# Check if part type exists by type_name and type_unit
@db_connector
def check_if_part_type_exists(type_name, type_unit, **kwargs):
    connection = kwargs.pop('connection')
    stmt = (select(PartType.type_name, PartType.type_unit).where(PartType.type_name == type_name
                                                                 and PartType.type_unit == type_unit))
    results = connection.execute(stmt).fetchone()
    if results:
        return True
    else:
        return False


class DBMUnitTest(TestCase):
    # Checks the different functions that interact with the parts database
    def test_parts_delete(self):
        print('test_parts_delete() TEST')
        part_name = random_string + random_time_string
        part_number = random_numbers + random_time_string
        part_store_name = random_string + random_time_string
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Create a partStore in the database
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        # Make sure it exist
        self.assertTrue(dbm.check_if_exists(part_store_name))
        # Add a part into the database
        dbm.insert(part_name=part_name, part_number=part_number, part_amount=random_digit,
                   part_store_name=part_store_name, part_type=part_type)
        # Check if it exists
        self.assertTrue(check_if_part_exist(part_name=part_name, part_number=part_number, part_amount=random_digit,
                                            part_store_name=part_store_name, part_type=part_type))
        print('insert() TRUE test -> PASSED')
        # Delete the newly added part by deleting the partStore
        dbm.delete_part_store(str(part_store_id))
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Make sure the corresponding partStore and part do not exist
        self.assertFalse(check_if_part_exist(part_name=part_name, part_number=part_number,
                                             part_amount=random_digit, part_store_name=part_store_name,
                                             part_type=part_type))
        self.assertFalse(check_if_part_store_exists(part_store_id))
        print('delete() test -> PASSED')

    def test_parts_update(self):
        print('test_parts_update() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Create another partStore
        dbm.insert_part_store(random_time_string, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        # Add another part into the database
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   part_store_name=random_time_string, part_type=part_type)
        # Get last part ID from the initial insert statement
        update_part_id = get_last_id(Part)[0]
        # Check that it exists, again
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=random_time_string, part_type=part_type))
        # Update it
        dbm.update(update_part_id, part_name=random_string + random_string, part_number=random_numbers + random_numbers,
                   part_store_name=random_time_string, part_amount=random_digit + random_digit, part_type=part_type)
        # Check that it exists
        self.assertTrue(
            check_if_part_exist(part_name=random_string + random_string, part_number=random_numbers + random_numbers,
                                part_store_name=random_time_string, part_amount=random_digit + random_digit,
                                part_type=part_type))
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete it
        dbm.delete_part_store(part_store_id)
        # Check existence
        self.assertFalse(
            check_if_part_exist(part_name=random_string + random_digit, part_number=random_numbers + random_digit,
                                part_store_name=random_time_string + random_digit,
                                part_amount=random_digit + random_digit,
                                part_type=part_type))
        self.assertFalse(check_if_part_store_exists(part_store_id))
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

    # Tests the insert_part_store function
    def test_insert_part_store(self):
        print('test_insert_part_store() TEST')
        # Create a test_insert_part_store with a random string of numbers
        part_store_name = 'test_part_store' + random_string
        # Insert it into the database
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        # Assert that check_if_exists will return True
        self.assertTrue(dbm.check_if_exists(part_store_name))
        print('insert_part_store() test -> PASSED')
        # Get the lastrowid and delete it from the database
        dbm.delete_part_store(part_store_id)
        # Assert that check_if_exists will return False since it is now deleted
        self.assertFalse(dbm.check_if_exists(part_store_name))
        print('insert_part_store() FALSE test -> PASSED')

    # Tests the delete_part_store function
    def test_delete_part_store(self):
        print('test_delete_part_store() TEST')
        # Create a test_part_store with a random digit
        part_store_name = 'test_part_store' + random_digit
        # Insert it into the database
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        # Get the part_store_id from the last insert statement
        part_store_id = get_last_id(PartStore)[0]
        # Delete the partStore from the database after getting the lastrowid
        dbm.delete_part_store(part_store_id)
        # Check if it exists in the database after deleting
        self.assertFalse(dbm.check_if_exists(part_store_name))
        print('delete_part_store() test -> PASSED')

    # Tests the update_part_store function
    def test_update_part_store(self):
        print('test_update_part_store() TEST')
        # Create a partStore with a random string
        part_store_name = 'test_update_part_store' + random_string
        # part store name to be updated to
        new_part_store_name = 'new_part_store_name' + random_string
        # Insert it into the database
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        # Get the row id after inserting
        part_store_id = get_last_id(PartStore)[0]
        # Update it to a new partStore name
        dbm.update_part_store(part_store_id, new_part_store_name, part_store_image=get_random_icon())
        # Check if the partStore exists
        self.assertTrue(dbm.check_if_exists(new_part_store_name))
        # Make sure if the partStore name is Blank, a TypeError is raised
        dbm.update_part_store(part_store_id, '', part_store_image=get_random_icon())
        self.assertRaises(TypeError)
        print('update_part_store() TypeError test -> PASSED')
        # When finished, delete the partStore from the database
        dbm.delete_part_store(part_store_id)
        # Make sure this operation was successful
        self.assertFalse(dbm.check_if_exists(new_part_store_name))
        print('update_part_store() test -> PASSED')

    # Tests the check_duplicates function
    def test_check_duplicates(self):
        print('test_check_duplicates() TEST')
        # Create a part_store name with a string of random numbers
        part_store_name = 'test_part_store' + random_numbers
        # Insert it into the database
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        # Get the lastrowid and delete it
        part_store_id = get_last_id(PartStore)[0]
        # Assert that check_duplicates will return false as it exists in the database
        self.assertFalse(dbm.check_duplicates(part_store_name))
        print('check_duplicates() duplicate part store FALSE test -> PASSED')
        dbm.delete_part_store(part_store_id)
        # Since it is now deleted, check if check_duplicates will return True
        self.assertTrue(dbm.check_duplicates(part_store_name))
        print('check_duplicates() duplicate part store TRUE test -> PASSED')

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
        dbm.register(username=username, password=password, conf_password=password,
                     phone_num=getenv('TEST_PHONE'))
        last_id = get_last_id(Account)[0]
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
        dbm.register(username, password, password, getenv('TEST_PHONE'))
        # Get account id
        acc_id = get_last_id(Account)[0]
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
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Create test partStore
        dbm.insert_part_store(random_time_string, part_store_icon=get_random_icon())
        # Get the partStore ID
        part_store_id = get_last_id(PartStore)[0]
        # Make sure it exists
        self.assertTrue(check_if_part_store_exists(part_store_id))
        # Insert a random part into the database with random values
        dbm.insert(random_string, random_digit, random_digit, random_time_string, part_type)
        # Make sure it was inserted into the database
        self.assertTrue(check_if_part_exist(random_string, random_digit, random_digit, random_time_string, part_type))
        print('insert() part amount TRUE test -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore and the part that it contains when finished
        dbm.delete_part_store(part_store_id)
        # Make sure it was deleted
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_numbers,
                                             part_number=random_digit, part_store_name=random_time_string,
                                             part_type=part_type))
        self.assertFalse(check_if_part_store_exists(part_store_id))
        print('insert() part amount FALSE test -> PASSED')

    # Test invalid input in the part amount attribute column
    def test_false_part_amount(self):
        print('test_false_part_amount() TEST')
        # Insert a part into the database with invalid part values (string where it is expecting an int)
        dbm.insert(part_name=random_string, part_amount=random_string, part_number=random_digit,
                   part_store_name=random_digit, part_type=random_string)
        # Make sure it was rejected from the database
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_numbers,
                                             part_number=random_digit, part_store_name=random_digit,
                                             part_type=random_string))
        print('insert() part amount invalid input test -> PASSED')

    # Test updating the part amount into the database
    def test_update_part_amount(self):
        print('test_update_part_amount() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Insert partStore number into database
        dbm.insert_part_store(random_time_string, part_store_icon=get_random_icon())
        # Get partStore ID
        part_store_id = get_last_id(PartStore)[0]
        # Check if it exists
        self.assertTrue(dbm.check_if_exists(random_time_string))
        # Insert a random part into the database
        dbm.insert(part_name=random_string, part_amount=random_digit + random_digit, part_number=random_digit,
                   part_store_name=random_time_string, part_type=part_type)
        # Get the ID of the last inserted part
        part_id = get_last_id(Part)[0]
        # Make sure it exists
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_digit + random_digit,
                                            part_number=random_digit, part_store_name=random_time_string,
                                            part_type=part_type))
        print('insert() part amount update insert test -> PASSED')
        # Update the part with random values
        dbm.update(part_id, part_name=random_string, part_amount=random_time_string, part_number=random_digit,
                   part_store_name=random_time_string, part_type=part_type)
        # Make sure the part exists based on these random values
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_time_string,
                                            part_number=random_digit, part_store_name=random_time_string,
                                            part_type=part_type))
        print('insert() part amount update test -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore and the part that it contains when finished
        dbm.delete_part_store(part_store_id)
        # Make sure the part and partStore was actually deleted
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_time_string,
                                             part_number=random_digit, part_store_name=random_time_string,
                                             part_type=part_type))
        self.assertFalse(check_if_part_store_exists(part_store_id))

    # Test the toggling of accounts to have admin privileges in the is_admin attribute
    def test_toggle_admin(self):
        print('test_toggle_admin() TEST')
        # Register a random user account
        dbm.register(username=username, password=password, conf_password=password,
                     phone_num=getenv('TEST_PHONE'))
        this_id = get_last_id(Account)[0]
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
        # Insert random partStore into database
        dbm.insert_part_store(this_string, part_store_icon=get_random_icon())
        this_id = get_last_id(PartStore)[0]
        # Make sure the method returns the string that was inserted
        self.assertIn(member=(this_string, this_string), container=dbm.get_selections())
        print('get_selections TEST -> PASSED')
        # Delete when finished
        dbm.delete_part_store(this_id)
        # Make sure the partStore has been deleted
        self.assertFalse(check_if_part_store_exists(this_id))
        print('check_if_part_store_exist() TEST -> PASSED')

    # Check the updating of the partStore on a part in the update function
    def test_update_parts_store(self):
        print('test_update_parts() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Create a new partStore
        dbm.insert_part_store(random_time_string, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        # Get random partStore from existing part store
        random_part_store = get_random_part_store()
        # Get the first partStore
        self.assertTrue(dbm.check_if_exists(random_time_string))
        print('insert_part_store TEST -> PASSED')
        # Add part to new partStore
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   part_store_name=random_time_string, part_type=part_type)
        part_id = get_last_id(Part)[0]
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=random_time_string, part_type=part_type))
        # Update the part with a random partStore that already exists
        dbm.update(part_id, part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   part_store_name=random_part_store, part_type=part_type)
        # Check if the part exists with the existing partStore
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=random_part_store, part_type=part_type))
        # Update the part to be back in its original partStore
        dbm.update(part_id, part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   part_store_name=random_time_string, part_type=part_type)
        # Make sure it exists
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=random_time_string, part_type=part_type))
        print('update TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore and it's containing part
        dbm.delete_part_store(part_store_id)
        # Make sure neither exist
        self.assertFalse(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=random_time_string, part_type=part_type))
        self.assertFalse(check_if_part_store_exists(part_store_id))
        print('test_update_parts() TEST -> PASSED')

    def test_create_job(self):
        print('test_create_job() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        part_store_name = random_time_string + digits + random_string
        # Create a random partStore
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        # Make sure that you cannot create a job from a partStore with no parts
        dbm.record_job(username=random_string, time=random_time_string + random_digit,
                       part_store_name=part_store_name,
                       parts_used=random_numbers)
        self.assertFalse(check_if_job_exists(_username=random_string,
                                             _time=random_time_string + random_digit,
                                             part_store=part_store_name, parts_used=random_numbers))
        print('create job FALSE TEST -> PASSED')
        # Insert part, check if it exists
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   part_store_name=part_store_name, part_type=part_type)
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=part_store_name, part_type=part_type))
        # Create job, make sure it exists
        dbm.record_job(username=random_string, time=random_time_string, part_store_name=part_store_name,
                       parts_used=random_digit)
        self.assertTrue(check_if_job_exists(_username=random_string, _time=random_time_string,
                                            part_store=part_store_name, parts_used=random_digit))
        print('create job TRUE TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore when finished
        dbm.delete_part_store(part_store_id)
        self.assertFalse(check_if_job_exists(random_string, random_time_string + random_digit,
                                             part_store_name, random_numbers))
        self.assertFalse(check_if_part_store_exists(part_store_id))
        print('test_create_job() TEST -> PASSED')

    # Test if the part difference is zero to not let the job enter the database
    def test_job_part_difference(self):
        print('test_job_part_difference() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Insert partStore into database
        part_store_name = random_numbers
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        self.assertTrue(check_if_part_store_exists(part_store_id))
        # Insert part into database
        dbm.insert(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                   part_store_name=part_store_name, part_type=part_type)
        self.assertTrue(
            check_if_part_exist(part_name=random_string, part_number=random_numbers, part_amount=random_digit,
                                part_store_name=part_store_name, part_type=part_type))
        # Make sure a job will not be recorded if the parts used is 0
        dbm.record_job(random_string, random_time_string + random_digit, part_store_name, parts_used=0)
        self.assertFalse(check_if_job_exists(_username=random_string, _time=random_time_string,
                                             part_store=part_store_name, parts_used=0))
        print('record_job FALSE TEST -> PASSED')
        dbm.record_job(random_string, random_time_string + random_digit, part_store_name, parts_used=random_digit)
        self.assertTrue(check_if_job_exists(_username=random_string, _time=random_time_string + random_digit,
                                            part_store=part_store_name, parts_used=random_digit))
        print('record_job TRUE TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore when finished
        dbm.delete_part_store(part_store_id)
        self.assertFalse(check_if_job_exists(_username=random_string, _time=random_time_string + random_digit,
                                             part_store=part_store_name, parts_used=random_digit))
        self.assertFalse(check_if_part_store_exists(part_store_id))
        print('test_job_part_difference() TEST -> PASSED')

    def test_enter_low_threshold(self):
        print('test_enter_low_threshold() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        part_store_name = random_digit + random_digit + random_string
        # Insert partStore
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        # First digit from range 1-5
        start_digit = ''.join(choice(digits) for z in range(1, 5))
        # Second digit from range 6-15
        thresh_digit = ''.join(choice(digits) for z in range(6, 15))
        # Insert random part into the partStore just created
        dbm.insert(random_string, start_digit, random_string, part_store_name, part_type)
        part_id = get_last_id(Part)[0]
        # Make sure the part exists
        self.assertTrue(check_if_part_exist(random_string, start_digit, random_string, part_store_name, part_type))
        print('insert part TEST -> PASSED')
        # Make sure the ID of the low part exists in the low parts table
        dbm.update_threshold(thresh_digit, part_id)
        self.assertEqual(part_id, get_low_part_id())
        # Make it higher
        dbm.update_threshold(start_digit, part_id)
        self.assertNotEqual(part_id, get_low_part_id())
        print('update threshold TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore when finished
        dbm.delete_part_store(part_store_id)
        self.assertFalse(check_if_part_store_exists(part_store_id))
        self.assertFalse(check_if_part_exist(random_string, start_digit, random_string, part_store_name, part_type))
        print('test_enter_low_threshold() TEST -> PASSED')

    def test_invalid_threshold(self):
        print('test_invalid_low_threshold() TEST')
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        part_store_name = random_digit + random_digit + random_time_string
        # Insert partStore
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        part_store_id = get_last_id(PartStore)[0]
        neg_digit = '-' + ''.join(choice(digits) for _ in range(1, 5))
        # First digit from range 1-5
        start_digit = ''.join(choice(digits) for _ in range(1, 5))
        # Insert random part into the partStore just created
        dbm.insert(random_string, start_digit, random_string, part_store_name, part_type)
        part_id = get_last_id(Part)[0]
        # Make sure the part exists
        self.assertTrue(check_if_part_exist(random_string, start_digit, random_string, part_store_name, part_type))
        print('insert part TEST -> PASSED')
        # Make sure the part doesn't appear in the low table at all if it is negative
        dbm.update_threshold(neg_digit, part_id)
        self.assertNotEqual(part_id, get_low_part_id())
        # Make it a character so it fails
        dbm.update_threshold(random_string, part_id)
        self.assertNotEqual(part_id, get_low_part_id())
        print('update threshold INVALID TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete the partStore when finished
        dbm.delete_part_store(part_store_id)
        self.assertFalse(check_if_part_store_exists(part_store_id))
        self.assertFalse(check_if_part_exist(random_string, start_digit, random_string, part_store_name, part_type))
        print('test_enter_invalid_threshold() TEST -> PASSED')

    def test_type_insertion(self):
        print('test_type_insertion() TEST')
        # Create random part type
        part_type = random_string + random_digit
        part_unit = random_string
        part_store_name = random_string + random_digit
        dbm.insert_part_store(part_store_name, part_store_icon=get_random_icon())
        self.assertTrue(dbm.check_if_exists(part_store_name))
        part_store_id = get_last_id(PartStore)[0]
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        print('Type Insertion TEST -> PASSED')
        # Add type to part
        dbm.insert(part_name=random_string, part_amount=random_digit, part_number=random_numbers,
                   part_store_name=part_store_name, part_type=part_type)
        self.assertTrue(check_if_part_exist(part_name=random_string,
                                            part_amount=random_digit, part_number=random_numbers,
                                            part_store_name=part_store_name, part_type=part_type))
        print('Insert Part TEST -> PASSED')
        self.assertIn(part_type, dbm.get_part_type_names())
        print('Check Part Type TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        # Delete part store
        dbm.delete_part_store(part_store_id)
        self.assertFalse(check_if_part_store_exists(part_store_id))
        print('test_type_insertion() TEST -> PASSED')

    def test_type_update(self):
        print('test_type_update() TEST')
        # Create random part type
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        print('Insert Type TEST -> PASSED')
        dbm.update_part_type(type_id=type_id, type_name=random_string, type_unit=random_string + random_digit)
        self.assertTrue(check_if_part_type_exists(type_name=random_string, type_unit=random_string + random_digit))
        print('Update Type TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        print('test_type_update() TEST -> PASSED')

    def test_type_duplicate_insertion(self):
        print('test_type_duplicate_insertion() TEST')
        # Create random part type
        part_type = random_string + random_digit
        part_unit = random_string
        # Insert part type
        dbm.insert_part_type(part_type, part_unit)
        type_id = get_last_id(PartType)[0]
        print('Insert Type TEST -> PASSED')
        # Make sure it exists
        self.assertTrue(check_if_type_exist(type_id))
        # Insert the same part type/unit
        dbm.insert_part_type(part_type, part_unit)
        # Make sure the part type is not duplicated
        dupe_count = get_part_type_duplicates(part_type)
        self.assertLess(dupe_count[0], 2)
        print('Type Duplicate TEST -> PASSED')
        # Delete part type
        dbm.delete_part_type(type_id)
        # Make sure it is deleted
        self.assertFalse(check_if_type_exist(type_id))
        print('test_type_duplicate_insertion() TEST -> PASSED')

    # Test validate phone number
    def test_validate_phone_number(self):
        print('test_validate_phone_number() TEST')
        # Create account, make sure it works
        self.assertEqual(dbm.register(username, password, password, getenv('TEST_PHONE')), 200)
        user_id = get_last_id(Account)[0]
        print('Valid Number TEST -> PASSED')
        # Try to create another account using the same number, make sure the process fails
        self.assertEqual(dbm.register(username, password, password, getenv('TEST_PHONE')), 409)
        print('Existing Number TEST -> PASSED')
        # Insert fake number into database
        self.assertEqual(dbm.register(username, password, password, random_phone_num_generator()), 409)
        print('Random Number TEST -> PASSED')
        # Delete the account when finished
        dbm.delete_account(user_id)
        # Make sure it is deleted
        self.assertFalse(dbm.check_if_account_exists(username))
        print('test_validate_phone_number() TEST -> PASSED')

    # Test the phone validation methods
    def test_phone_num_methods(self):
        print('test_phone_num_methods() TEST')
        # Make sure a random number doesn't exist in the database
        self.assertFalse(dbm.check_if_phone_num_exists(random_phone_num_generator()))
        print('Random Number EXISTENCE FALSE TEST -> PASSED')
        # Make sure a random number is not valid
        self.assertFalse(check_phone_num(random_phone_num_generator()))
        print('Random Number VALIDITY FALSE TEST -> PASSED')
        # Make sure a real number exists
        self.assertTrue(check_phone_num(getenv('TEST_PHONE')))
        # Make sure a number that is inserted into the database exists
        dbm.register(username, password, password, getenv('TEST_PHONE'))
        user_id = get_last_id(Account)[0]
        self.assertTrue(dbm.check_if_phone_num_exists(getenv('TEST_PHONE')))
        print('Random Number EXISTENCE TRUE TEST -> PASSED')
        # Delete when finished
        dbm.delete_account(user_id)
        # Make sure it is deleted
        self.assertFalse(dbm.check_if_account_exists(username))
        print('test_phone_num_methods() TEST -> PASSED')

    # Test to make sure blank input will not be added into the database
    def test_part_store_input(self):
        print('test_part_store_input() TEST')
        dbm.insert_part_store(random_string, '')
        self.assertFalse(check_part_store_name(random_string))
        print('Blank icon name TEST -> PASSED')
        dbm.insert_part_store('', get_random_icon())
        self.assertFalse((check_part_store_name('')))
        print('Blank part store name TEST -> PASSED')
        dbm.insert_part_store('', '')
        self.assertFalse(check_part_store_name(''))
        print('Blank part store name and icon TEST -> PASSED')

    # Test the store icon names functionality
    def test_icon_names(self):
        print('test_store_icon_names() TEST')
        icon = get_random_icon()
        dbm.insert_part_store(random_string, part_store_icon=icon)
        part_store_id = get_last_id(PartStore)[0]
        self.assertTrue(dbm.check_if_exists(random_string))
        print('Insert van TEST -> PASSED')
        self.assertEqual(get_current_store_name_icon(part_store_id)[1], icon)
        print('Icon equal TEST -> PASSED')
        dbm.delete_part_store(part_store_id)
        self.assertFalse(dbm.check_if_exists(random_string))
        print('test_store_icon_names() TEST -> PASSED')


if __name__ == '__main__':
    main()
