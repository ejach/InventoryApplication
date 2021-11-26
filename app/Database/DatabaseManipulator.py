from bcrypt import gensalt, hashpw, checkpw
from pymysql import Error

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseStatements import DatabaseStatements


# Prevents inputs that only contain spaces from being entered into the database
def check_input(test_input):
    if not test_input or test_input.isspace():
        return False
    else:
        return True


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


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.cursor = self.db.get_cursor()
        self.conn = self.db.get_conn()
        self.stmt = DatabaseStatements()

    # Get all parts entries from database
    def fetchall(self):
        try:
            self.conn.ping()
            stmt = self.stmt.get_select_statement()
            self.cursor.execute(stmt)
            results = self.cursor.fetchall()
            self.conn.close()
            return results
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Checks to see if the van_number exists in the database already
    def check_duplicates(self, van_number):
        try:
            self.conn.ping()
            stmt = self.stmt.get_vans_dupes()
            self.cursor.execute(stmt)
            results = self.cursor.fetchall()
            res = [i[0] for i in results]
            if res.count(van_number) > 0:
                return False
            else:
                return True
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Get password by username
    def get_password_by_username(self, username):
        try:
            self.conn.ping()
            stmt = self.stmt.get_check_if_username_exists()
            values = (username,)
            self.cursor.execute(stmt, values)
            username_res = self.cursor.fetchall()
            fin_res = [i[2] for i in username_res]
            return fin_res
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Check if account exists in the database
    def check_if_account_exists(self, username):
        try:
            self.conn.ping()
            stmt = self.stmt.get_check_if_username_exists()
            values = (username,)
            self.cursor.execute(stmt, values)
            get_username_results = self.cursor.fetchall()
            if not get_username_results:
                return False
            else:
                return True
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Check if the van exists and has a part within it from either the parts or vans DB
    def check_if_exists(self, van_number):
        try:
            self.conn.ping()
            # Use the distinct select statement in the parts DB
            get_vans_dist = self.stmt.get_select_vans_distinct()
            self.cursor.execute(get_vans_dist)
            dist_results = self.cursor.fetchall()
            # List the results in an array
            fin_dist = [i[0] for i in dist_results]
            # Use the list of duplicates to see if the van exists in the vans DB
            get_duplicates = self.stmt.get_vans_dupes()
            self.cursor.execute(get_duplicates)
            dupe_results = self.cursor.fetchall()
            self.conn.close()
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
        try:
            # If the input is valid and the check_duplicates is valid, commit to DB
            if self.check_duplicates(van_number) and check_input(van_number):
                self.conn.ping()
                stmt = self.stmt.get_insert_van()
                val = (van_number,)
                self.cursor.execute(stmt, val)
                self.conn.close()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, row not inserted')
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Get all vans by van number
    def get_vans(self, van_number):
        try:
            self.conn.ping()
            stmt = self.stmt.get_select_vans_statement()
            val = (van_number,)
            self.cursor.execute(stmt, val)
            results = self.cursor.fetchall()
            self.conn.close()
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
        self.conn.ping()
        try:
            stmt = self.stmt.get_select_vans_order_statement()
            self.cursor.execute(stmt)
            results = self.cursor.fetchall()
            self.conn.close()
            return results
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Insert entries into database
    def insert(self, part_name, part_number, van_number):
        try:
            self.conn.ping()
            stmt = self.stmt.get_insert_statement()
            values = (part_name, part_number, van_number)
            if check_input(part_name) and check_input(part_number) and check_input(van_number):
                self.cursor.execute(stmt, values)
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, row not inserted')
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Delete entries from database by ID
    def delete(self, row_id):
        try:
            self.conn.connect()
            stmt = self.stmt.get_delete_statement()
            self.cursor.execute(stmt, (int(row_id),))
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Update entries from database by ID
    def update(self, row_id, part_name, part_number, van_number):
        try:
            self.conn.ping()
            stmt = self.stmt.get_update_statement()
            values = (part_name, part_number, van_number, int(row_id))
            if check_input(part_name) and check_input(part_number) and check_input(van_number):
                self.cursor.execute(stmt, values)
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, database not manipulated')
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Delete van by van_id
    def delete_van(self, van_id):
        try:
            self.conn.ping()
            stmt = self.stmt.get_delete_van()
            self.cursor.execute(stmt, (int(van_id),))
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Update van by van_id
    def update_van(self, van_id, van_number):
        try:
            # Check for duplicates and validate input
            if check_input(van_number) and self.check_duplicates(van_number):
                self.conn.ping()
                stmt = self.stmt.get_update_van()
                values = (van_number, int(van_id),)
                self.cursor.execute(stmt, values)
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, database not manipulated')
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()

    # Login by username and password
    def login(self, username, password):
        try:
            hash_pw = self.get_password_by_username(username)
            if check_password_hash(password.encode('utf8'), hash_pw[0].encode('utf8')) \
                    and self.check_if_account_exists(username):
                return True
            else:
                return False
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')

    # Register by username, password, and conf_password
    def register(self, username, password, conf_password):
        try:
            stmt = self.stmt.get_register()
            if check_password(password, conf_password) and check_input(password) and check_input(conf_password) \
                    and not self.check_if_account_exists(username):
                hashed_pw = create_password_hash(password.encode('utf-8'))
                if check_password_hash(password.encode('utf-8'), hashed_pw):
                    self.conn.ping()
                    values = (username, hashed_pw,)
                    self.cursor.execute(stmt, values)
        except Error as e:
            print(str(e) + '\n' + 'Lost connection to the MySQL server.')
        finally:
            if self.conn is not None:
                self.conn.close()
