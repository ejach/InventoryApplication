# SQL Statements that are only used in a unit testing environment
from app.Database.DatabaseConnector import DatabaseConnector


class TestDatabaseStatements:
    def __init__(self):
        self.dbc = DatabaseConnector()
        self.db = self.dbc.get_db()
        self.delete_account_by_id = f'DELETE FROM {self.db}.accounts WHERE id = %s'
        self.get_last_id = 'SELECT MAX( id ) FROM parts'
        self.check_part_existence = f'SELECT * FROM {self.db}.parts WHERE name = %s AND amount = %s AND part_number = %s AND van_number = %s'
        self.check_van_existence = f'SELECT * FROM {self.db}.vans WHERE id = %s'
        self.check_job_existence = f'SELECT * FROM {self.db}.jobs WHERE username = %s AND time = %s AND van_number = %s AND parts_used = %s'
        self.get_random_van = f'SELECT `van_number` FROM {self.db}.vans ORDER BY RAND() LIMIT 1;'
        self.get_random_username = f'SELECT `username` FROM {self.db}.accounts ORDER BY RAND() LIMIT 1;'
        self.delete_job_by_id = f'DELETE FROM {self.db}.jobs WHERE job_id = %s'

    def get_delete_account_by_id(self):
        return self.delete_account_by_id

    def get_get_last_id(self):
        return self.get_last_id

    def get_check_part_existence(self):
        return self.check_part_existence

    def get_check_van_existence(self):
        return self.check_van_existence

    def get_get_random_van(self):
        return self.get_random_van

    def get_delete_job_by_id(self):
        return self.delete_job_by_id

    def get_get_random_username(self):
        return self.get_random_username

    def get_check_job_existence(self):
        return self.check_job_existence
