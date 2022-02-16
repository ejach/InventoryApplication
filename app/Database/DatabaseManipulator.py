from bcrypt import gensalt, hashpw, checkpw
from pymysql import Error

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseStatements import DatabaseStatements


# Prevent inputs that only contain spaces from being entered into the database
def check_input(test_input):
    if test_input and not test_input.isspace() and '-' not in test_input:
        return True
    else:
        return False


# Create MD5 hash of password to insert into database
def create_password_hash(password):
    salt = gensalt()
    hashed = hashpw(password, salt)
    if check_password_hash(password, hashed):
        return hashed


# Check if the password is equal to each other
def check_password(password, conf_password):
    if password == conf_password:
        return True
    else:
        return False


# Check if MD5 hash matches the password given
def check_password_hash(password, my_hash):
    if checkpw(password, my_hash):
        return True
    else:
        return False


# get difference of two values
def get_difference(op1, op2):
    if op1 > op2:
        return op1 - op2
    elif op1 < op2:
        return op2 - op1
    elif op1 == op2:
        return op1 - op2


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.stmt = DatabaseStatements()

    # Get all parts entries from database
    def fetchall(self):
        with self.db.get_conn() as cursor:
            stmt = self.stmt.get_select_statement()
            cursor.execute(stmt)
            results = cursor.fetchall()
            return results

    # Checks to see if the van_number exists in the database already
    def check_duplicates(self, van_number):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_vans_dupes()
                cursor.execute(stmt)
                results = cursor.fetchall()
                res = [i[0] for i in results]
                if res.count(van_number) > 0:
                    return False
                else:
                    return True
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get password by username
    def get_password_by_username(self, username):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_check_if_username_exists()
                values = (username,)
                cursor.execute(stmt, values)
                username_res = cursor.fetchall()
                fin_res = [i[2] for i in username_res]
                return fin_res
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Check if account exists in the database
    def check_if_account_exists(self, username):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_check_if_username_exists()
                values = (username,)
                cursor.execute(stmt, values)
                get_username_results = cursor.fetchall()
                if not get_username_results:
                    return False
                else:
                    return True
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Check if the van exists and has a part within it from either the parts or vans DB
    def check_if_exists(self, van_number):
        with self.db.get_conn() as cursor:
            try:
                # Use the distinct select statement in the parts DB
                get_vans_dist = self.stmt.get_select_vans_distinct()
                cursor.execute(get_vans_dist)
                dist_results = cursor.fetchall()
                # List the results in an array
                fin_dist = [i[0] for i in dist_results]
                # Use the list of duplicates to see if the van exists in the vans DB
                get_duplicates = self.stmt.get_vans_dupes()
                cursor.execute(get_duplicates)
                dupe_results = cursor.fetchall()
                # List the results in an array
                fin_dupes = [i[0] for i in dupe_results]
                # If the van_number exists in either database, return True; otherwise return False
                if fin_dist.count(van_number) > 0 or van_number in fin_dupes:
                    return True
                else:
                    return False
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Insert van into the database
    def insert_van(self, van_number):
        with self.db.get_conn() as cursor:
            try:
                # If the input is valid and the check_duplicates is valid, commit to DB
                if self.check_duplicates(van_number) and check_input(van_number):
                    stmt = self.stmt.get_insert_van()
                    val = (van_number,)
                    cursor.execute(stmt, val)
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, row not inserted')
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get all vans by van number
    def get_vans(self, van_number):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_select_vans_statement()
                val = (van_number,)
                cursor.execute(stmt, val)
                results = cursor.fetchall()
                # If the results are empty (i.e. the van_number doesn't exist) return None
                if not results:
                    return None
                # Else, return the following
                else:
                    return results
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get list of van numbers that exist in the database
    def get_van_nums(self):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_select_vans_order_statement()
                cursor.execute(stmt)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get the selections from the Vans that currently exist in the database
    def get_selections(self):
        results = self.get_van_nums()
        re = [(g[1], g[1]) for g in results]
        return re

    # Insert entries into database
    def insert(self, part_name, part_amount, part_number, van_number):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_insert_statement()
                values = (part_name, part_amount, part_number, str(van_number))
                if check_input(part_name) and check_input(part_amount) and part_amount.isnumeric() \
                        and check_input(part_number) and check_input(van_number):
                    cursor.execute(stmt, values)
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, row not inserted')
            except Error as e:
                print(str(e))

    # Get part information by part id
    def get_part_information(self, part_id):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_select_part_by_id()
                cursor.execute(stmt, part_id)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(str(e))

    # Delete entries from database by ID
    def delete(self, row_id):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_delete_statement()
                cursor.execute(stmt, (int(row_id),))
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Update entries from database by ID
    def update(self, row_id, part_name, part_amount, part_number, van_number):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_update_statement()
                values = (part_name, int(part_amount), part_number, van_number, int(row_id))
                if check_input(part_name) and check_input(part_amount) and check_input(part_number) \
                        and check_input(van_number):
                    cursor.execute(stmt, values)
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, database not manipulated')
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Delete van by van_id
    def delete_van(self, van_id):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_delete_van()
                cursor.execute(stmt, (int(van_id),))
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Update van by van_id
    def update_van(self, van_id, van_number):
        with self.db.get_conn() as cursor:
            try:
                # Check for duplicates and validate input
                if check_input(van_number) and self.check_duplicates(van_number):
                    stmt = self.stmt.get_update_van()
                    values = (van_number, int(van_id),)
                    cursor.execute(stmt, values)
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, database not manipulated')
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Check if account is confirmed
    def check_if_confirmed(self, username):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.check_confirmed
                cursor.execute(stmt, username)
                results = cursor.fetchone()
                res = int(''.join(map(str, results)))
                if res == 1:
                    return True
                else:
                    return False
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Confirm account by ID
    def confirm_account(self, user_id):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.confirm_account
                cursor.execute(stmt, user_id)
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Delete account by ID
    def delete_account(self, user_id):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.delete_account
                cursor.execute(stmt, user_id)
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Login by username and password
    def login(self, username, password):
        try:
            hash_pw = self.get_password_by_username(username)
            if hash_pw and check_password_hash(password.encode('utf8'), hash_pw[0].encode('utf8')) \
                    and self.check_if_account_exists(username) and self.check_if_confirmed(username):
                return True
            else:
                return False
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Register by username, password, and conf_password
    def register(self, username, password, conf_password):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_register()
                if check_password(password, conf_password) and check_input(password) and check_input(conf_password) \
                        and not self.check_if_account_exists(username):
                    hashed_pw = create_password_hash(password.encode('utf-8'))
                    if check_password_hash(password.encode('utf-8'), hashed_pw):
                        values = (username, hashed_pw,)
                        cursor.execute(stmt, values)
                    return True
                else:
                    return False
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Check if user is an admin by username
    def check_admin(self, username):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.check_admin
                cursor.execute(stmt, username)
                results = cursor.fetchall()
                res = int(''.join(map(str, results[0])))
                return res
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Make / remove user from admin
    def modify_admin(self, user_id, value):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_modify_admin()
                values = (value, user_id)
                cursor.execute(stmt, values)
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get users that exist in the DB excluding the current user's username
    def get_users(self, username):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_users
                cursor.execute(stmt, username)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get parts by van number
    def get_parts_by_van(self, van_number):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_select_parts_by_van()
                cursor.execute(stmt, van_number)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Update multiple parts according to the van number
    def update_multiple_parts_by_van(self, values):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_update_part_amount_by_van()
                cursor.executemany(stmt, values)
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Record a new job in the database
    def record_job(self, username, time, van_number, parts_used):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.insert_job
                vals = (username, time, van_number, parts_used)
                cursor.execute(stmt, vals)
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get all jobs from database
    def get_jobs(self):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.get_jobs
                cursor.execute(stmt)
                results = cursor.fetchall()
                return results
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get the total amount of parts by van
    def get_total_parts_by_van(self, van):
        with self.db.get_conn() as cursor:
            try:
                stmt = self.stmt.select_total_amount_by_van
                cursor.execute(stmt, van)
                results = cursor.fetchall()
                res = [i[0] for i in results]
                return res[0]
            except Error as e:
                print(str(e) + '\n' + 'Lost connection to the MySQL server.')
