from src.DatabaseConnector import DatabaseConnector


class DatabaseManipulator:
    def __init__(self):
        self.db = DatabaseConnector()
        self.cursor = self.db.cursor

    def fetchall(self):
        stmt = 'SELECT * FROM parts'
        self.cursor.execute(stmt)
        results = self.cursor.fetchall()
        return results
