from unittest import TestCase, main
from random import choice
from string import ascii_letters, digits

from app.Database.DatabaseManipulator import DatabaseManipulator, check_input
from app.Database.TestDatabaseStatements import TestDatabaseStatements

dbm = DatabaseManipulator()
tdbs = TestDatabaseStatements()

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))


# Get last id of entry that was inserted into the database
def get_last_id():
    get_id = tdbs.get_get_last_id()
    dbm.cursor.execute(get_id)
    id_res = dbm.cursor.fetchone()
    final_res = (','.join(str(a) for a in id_res))
    return str(final_res)


class DBMUnitTest(TestCase):
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


if __name__ == '__main__':
    main()
