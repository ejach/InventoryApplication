# SQL Statements that are only used in a unit testing environment
class TestDatabaseStatements:
    def __init__(self):
        self.delete_account_by_id = 'DELETE FROM parts.accounts WHERE id = %s'
        self.get_last_id = 'SELECT last_insert_id()'

    def get_delete_account_by_id(self):
        return self.delete_account_by_id

    def get_get_last_id(self):
        return self.get_last_id

