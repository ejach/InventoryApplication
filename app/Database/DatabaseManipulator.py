from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseStatements import DatabaseStatements


# Prevents inputs that only contain spaces from being entered into the database
def check_input(test_input):
    if not test_input or len(test_input) == 0 or test_input.isspace():
        return False
    else:
        return True


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.cursor = self.db.get_cursor()
        self.conn = self.db.get_conn()
        self.stmt = DatabaseStatements()

    # Get all entries from database
    def fetchall(self):
        stmt = self.stmt.get_select_statement()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        return results

    # Checks to see if the van_number exists in the database already
    def check_duplicates(self, van_number):
        stmt = self.stmt.get_vans_dupes()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        res = [i[0] for i in results]
        if res.count(van_number) > 0:
            return False
        else:
            return True

    # Check if the van exists and has a part within it from either the parts or vans DB
    def check_if_exists(self, van_number):
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
        # List the results in an array
        fin_dupes = [i[0] for i in dupe_results]
        # If the van_number exists in either database, return True; otherwise return False
        if fin_dist.count(van_number) > 0 or van_number in fin_dupes:
            return True
        else:
            return False

    # Insert van into the database
    def insert_van(self, van_number):
        try:
            # If the input is valid and the check_duplicates is valid, commit to DB
            if self.check_duplicates(van_number) and check_input(van_number):
                stmt = self.stmt.get_insert_van()
                val = (van_number,)
                self.cursor.execute(stmt, val)
                self.conn.commit()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, row not inserted')

    # Get all vans by van number
    def get_vans(self, van_number):
        stmt = self.stmt.get_select_vans_statement()
        val = (van_number,)
        self.cursor.execute(stmt, val)
        results = self.cursor.fetchall()
        # If the results are empty (i.e. the van_number doesn't exist) return None
        if not results:
            return None
        # Else, return the following
        else:
            return results

    # Get list of van numbers that exist in the database
    def get_van_nums(self):
        stmt = self.stmt.get_select_vans_order_statement()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        return results

    # Insert entries into database
    def insert(self, part_name, part_number, van_number):
        try:
            stmt = self.stmt.get_insert_statement()
            values = (part_name, part_number, van_number)
            self.cursor.execute(stmt, values)
            if check_input(part_name) and check_input(part_number) and check_input(van_number):
                self.conn.commit()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, row not inserted')

    # Delete entries from database by ID
    def delete(self, row_id):
        stmt = self.stmt.get_delete_statement()
        self.cursor.execute(stmt, (int(row_id),))
        self.conn.commit()

    # Update entries from database by ID
    def update(self, row_id, part_name, part_number, van_number):
        try:
            stmt = self.stmt.get_update_statement()
            values = (part_name, part_number, van_number, int(row_id))
            self.cursor.execute(stmt, values)
            if check_input(part_name) and check_input(part_number) and check_input(van_number):
                self.conn.commit()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, database not manipulated')

    # Delete van by van_id
    def delete_van(self, van_id):
        stmt = self.stmt.get_delete_van()
        self.cursor.execute(stmt, (int(van_id),))
        self.conn.commit()

    # Update van by van_id
    def update_van(self, van_id, van_number):
        try:
            # Check for duplicates and validate input
            if check_input(van_number) and self.check_duplicates(van_number):
                stmt = self.stmt.get_update_van()
                values = (van_number, int(van_id),)
                self.cursor.execute(stmt, values)
                self.conn.commit()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, database not manipulated')
