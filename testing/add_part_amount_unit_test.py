from random import choice
from string import ascii_letters, digits
from time import time
from unittest import TestCase, main

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator
from app.Database.TestDatabaseStatements import TestDatabaseStatements

random_string = ''.join(choice(ascii_letters) for x in range(10))
random_numbers = ''.join(choice(digits) for y in range(10))
random_digit = ''.join(choice(digits) for z in range(1))

dbm = DatabaseManipulator()
dbc = DatabaseConnector()
tdbs = TestDatabaseStatements()

# Gets the epoch time and truncates the trailing decimals
random_time_string = str(int(time()))


def get_last_id():
    get_id = tdbs.get_get_last_id()
    dbc.cursor.execute(get_id)
    id_res = dbc.cursor.fetchone()
    final_res = (','.join(str(a) for a in id_res))
    return str(final_res)

def check_if_part_exist(part_name, part_amount, part_number, van_number):
    dbc.conn.ping()
    get_part = tdbs.get_check_part_existence()
    values = (part_name, part_amount, part_number, van_number,)
    dbc.cursor.execute(get_part, values)
    results = dbc.cursor.fetchall()
    if not results:
        return False
    else:
        return True


class TestModifyPart(TestCase):
    def test_add_part_amount(self):
        dbm.insert(part_name=random_string, part_amount=random_numbers, part_number=random_digit,
                   van_number=random_digit)
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_numbers, part_number=random_digit, van_number=random_digit))
        print('insert() part amount TRUE test -> PASSED' + '\n')
        this_part = get_last_id()
        dbm.delete(this_part)
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_numbers, part_number=random_digit, van_number=random_digit))
        print('insert() part amount FALSE test -> PASSED' + '\n')

    def test_false_part_amount(self):
        dbm.insert(part_name=random_string, part_amount=random_string, part_number=random_digit,
                   van_number=random_digit)
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_numbers, part_number=random_digit, van_number=random_digit))
        print('insert() part amount invalid input test -> PASSED' + '\n')

    def test_update_part_amount(self):
        dbm.insert(part_name=random_string, part_amount=random_numbers, part_number=random_digit,
                   van_number=random_time_string)
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_numbers, part_number=random_digit, van_number=random_time_string))
        print('insert() part amount update insert test -> PASSED' + '\n')
        this_id = get_last_id()
        dbm.update(this_id, part_name=random_string, part_amount=random_time_string, part_number=random_digit,
                   van_number=random_digit)
        self.assertTrue(check_if_part_exist(part_name=random_string, part_amount=random_time_string, part_number=random_digit, van_number=random_digit))
        print('insert() part amount update test -> PASSED' + '\n')
        dbm.delete(this_id)
        self.assertFalse(check_if_part_exist(part_name=random_string, part_amount=random_time_string, part_number=random_digit, van_number=random_digit))


if __name__ == '__main__':
    main()
