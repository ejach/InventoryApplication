from json import dumps, loads

from src.DatabaseConnector import DatabaseConnector
from src.DatabaseStatements import DatabaseStatements


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.cursor = self.db.get_cursor()
        self.stmt = DatabaseStatements()

    # Get all entries from database
    def fetchall(self):
        stmt = self.stmt.get_select_stmt()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        return results

    # Insert entries into database
    def insert(self, part_name, part_number):
        stmt = self.stmt.get_insert_statement()
        self.cursor.execute(stmt, (part_name, part_number))
        self.db.database.commit()

    # Get all database entries and translate them into JSON
    def get_json(self):
        stmt = self.stmt.get_select_stmt()
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        container = []
        for tup in results:
            json_string = {'data': {tup[0]: {"name": tup[1], "part_number": tup[2]}}}
            j_dump = dumps(json_string, separators=(" , ", " : "))
            loader = loads(j_dump)
            container.append(loader)
        return container
