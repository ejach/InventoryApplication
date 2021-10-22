from json import dumps, loads

from src.DatabaseConnector import DatabaseConnector
from src.DatabaseStatements import DatabaseStatements


# Prevents inputs that only contain spaces from being entered into the database
def check_input(part_name, part_number):
    if not part_number and not part_number or not part_name.isspace() and not part_number.isspace():
        return True
    else:
        return False


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
        res = [i[0] for i in results]
        return res

    # Insert entries into database
    def insert(self, part_name, part_number, van_number):
        stmt = self.stmt.get_insert_statement()
        values = (part_name, part_number, van_number)
        self.cursor.execute(stmt, values)
        if check_input(part_name, part_number):
            self.conn.commit()

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
            if check_input(part_name, part_number):
                self.conn.commit()
        except TypeError as e:
            print(str(e) + '\n' + 'Blank input detected, database not manipulated')

    # Get all database entries and translate them into JSON
    def get_json(self):
        stmt = self.stmt.get_select_statement()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        container = []
        for tup in results:
            json_string = {'data': {tup[0]: {"name": tup[1], "part_number": tup[2]}}}
            j_dump = dumps(json_string, separators=(" , ", " : "))
            loader = loads(j_dump)
            container.append(loader)
        return container
