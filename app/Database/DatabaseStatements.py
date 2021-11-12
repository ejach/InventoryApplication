from app.Database.DatabaseConnector import DatabaseConnector


class DatabaseStatements:
    def __init__(self):
        self.dbc = DatabaseConnector()
        self.db = self.dbc.get_db()
        self.select = f'SELECT * FROM {self.db}.parts'
        self.select_vans = f'SELECT * FROM {self.db}.parts WHERE `van_number` = %s'
        self.select_vans_order = f'SELECT * FROM {self.db}.vans ORDER BY `van_number`'
        self.select_vans_distinct = f'SELECT DISTINCT `van_number` from {self.db}.parts ORDER BY `van_number`'
        self.select_vans_dupes = f'SELECT `van_number` from {self.db}.vans'
        self.insert_van = f'INSERT INTO {self.db}.vans (van_number) VALUE (%s)'
        self.delete_van = f'DELETE FROM {self.db}.vans WHERE `id` = %s'
        self.update_van = f'UPDATE {self.db}.vans SET `van_number` = %s WHERE `id` = %s'
        self.login = f'SELECT * FROM {self.db}.accounts WHERE `username` = %s AND `password` = %s'
        self.register = f'INSERT INTO {self.db}.accounts (username, password) VALUES (%s, %s)'
        self.check_if_username_exists = f'SELECT * FROM {self.db}.accounts WHERE `username` = %s'
        self.get_password_by_username = f'SELECT `password` FROM {self.db}.accounts WHERE `username` = %s'
        self.insert = f'INSERT INTO {self.db}.parts (name, part_number, van_number) VALUES (%s, %s, %s)'
        self.delete = f'DELETE FROM {self.db}.parts WHERE `id` = %s'
        self.update = f'UPDATE {self.db}.parts set `name` = %s, `part_number` = %s, `van_number` = %s WHERE `id` = %s'

    def get_select_statement(self):
        return self.select

    def get_select_vans_statement(self):
        return self.select_vans

    def get_select_vans_order_statement(self):
        return self.select_vans_order

    def get_select_vans_distinct(self):
        return self.select_vans_distinct

    def get_vans_dupes(self):
        return self.select_vans_dupes

    def get_insert_statement(self):
        return self.insert

    def get_login(self):
        return self.login

    def get_insert_van(self):
        return self.insert_van

    def get_delete_van(self):
        return self.delete_van

    def get_update_van(self):
        return self.update_van

    def get_delete_statement(self):
        return self.delete

    def get_update_statement(self):
        return self.update

    def get_register(self):
        return self.register

    def get_check_if_username_exists(self):
        return self.check_if_username_exists

    def get_password_by_username(self):
        return self.get_password_by_username
