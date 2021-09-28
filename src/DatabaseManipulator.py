from src.DatabaseConnector import DatabaseConnector
from src.DatabaseStatements import DatabaseStatements


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.cursor = self.db.get_cursor()
        self.stmt = DatabaseStatements()

    def fetchall(self):
        try:
            stmt = self.stmt.get_select_stmt()
            self.cursor.execute(stmt)
            results = self.cursor.fetchall()
            return results
        except:
            self.db.database.rollback()
            results = None
            return results

    def insert(self, part_name, part_number):
        stmt = self.stmt.get_insert_statement()
        self.cursor.execute(stmt, (part_name, part_number))
        self.db.database.commit()
