from src.DatabaseConnector import DatabaseConnector


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.cursor = self.db.cursor

    def fetchall(self):
        try:
            stmt = 'SELECT * FROM parts'
            self.cursor.execute(stmt)
            results = self.cursor.fetchall()
            error = ''
            return results, error
        except:
            self.db.database.rollback()
            results = None
            error = "Error connecting to the database"
            return results, error

    def insert(self, part_name, part_number):
        stmt = 'INSERT INTO parts (name, part_number) VALUES (?, ?)'
        self.cursor.execute(stmt, (part_name, part_number))
        self.db.database.commit()
