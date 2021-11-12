# SQL Statements that are only used in a unit testing environment
from app.Database.DatabaseConnector import DatabaseConnector

dbc = DatabaseConnector()


class TestDatabaseStatements:
    def __init__(self):
        self.db = dbc.get_db()
        self.delete_account_by_id = f'DELETE FROM {self.db}.accounts WHERE id = %s'
        self.get_last_id = 'SELECT last_insert_id()'
        self.check_part_existence = f'SELECT * FROM {self.db}.parts WHERE name = %s AND part_number = %s AND van_number = %s'

    def get_delete_account_by_id(self):
        return self.delete_account_by_id

    def get_get_last_id(self):
        return self.get_last_id

    def get_check_part_existence(self):
        return self.check_part_existence
