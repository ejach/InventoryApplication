from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseStatements import DatabaseStatements


# Prevents inputs that only contain spaces from being entered into the database
def check_input(part_name, part_number, van_number):
    if not part_name or not part_number or not van_number \
            or len(part_name) == 0 or len(part_number) == 0 or len(van_number) == 0 \
            or part_name.isspace() or part_number.isspace() or van_number.isspace():
        return False
    else:
        return True


# Checks if the van number is valid by seeing if it is a space/empty string or if it is a number
def check_van_number(van_number):
    if not van_number or van_number.isspace() or not van_number.isdigit():
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
        stmt = self.stmt.get_select_vans_distinct_statement()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        res = [i[0] for i in results]
        for num in res:
            if van_number == num:
                return False
            else:
                return True

    # Insert van into the database
    def insert_van(self, van_number):
        try:
            stmt = self.stmt.get_insert_van()
            val = (van_number,)
            self.cursor.execute(stmt, val)
            # If the input is valid and the check_duplicates is valid, commit to DB
            if check_van_number(van_number) and self.check_duplicates(van_number):
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
        stmt = self.stmt.get_select_vans_distinct_statement()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        return results

    # Insert entries into database
    def insert(self, part_name, part_number, van_number):
        try:
            stmt = self.stmt.get_insert_statement()
            values = (part_name, part_number, van_number)
            self.cursor.execute(stmt, values)
            if check_input(part_name, part_number, van_number):
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
            if check_input(part_name, part_number, van_number):
                self.conn.commit()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, database not manipulated')

    def delete_van(self, van_id):
        stmt = self.stmt.get_delete_van()
        self.cursor.execute(stmt, (int(van_id),))
        self.conn.commit()
