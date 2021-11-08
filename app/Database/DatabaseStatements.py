class DatabaseStatements:

    def __init__(self):
        self.select = 'SELECT * FROM parts.parts'
        self.select_vans = 'SELECT * FROM parts.parts WHERE `van_number` = %s'
        self.select_vans_order = 'SELECT * FROM parts.vans ORDER BY `van_number`'
        self.select_vans_distinct = 'SELECT DISTINCT `van_number` from parts.parts ORDER BY `van_number`'
        self.select_vans_dupes = 'SELECT `van_number` from parts.vans'
        self.insert_van = 'INSERT INTO parts.vans (van_number) VALUE (%s)'
        self.delete_van = 'DELETE FROM parts.vans WHERE `id` = %s'
        self.update_van = 'UPDATE parts.vans SET `van_number` = %s WHERE `id` = %s'
        self.login = 'SELECT * FROM parts.accounts WHERE `username` = %s AND `password` = %s'
        self.register = 'INSERT INTO parts.accounts (username, password) VALUES (%s, %s)'
        self.check_if_username_exists = 'SELECT * FROM parts.accounts WHERE `username` = %s'
        self.get_password_by_username = 'SELECT `password` FROM parts.accounts WHERE `username` = %s'
        self.insert = 'INSERT INTO parts.parts (name, part_number, van_number) VALUES (%s, %s, %s)'
        self.delete = 'DELETE FROM parts.parts WHERE `id` = %s'
        self.update = 'UPDATE parts.parts set `name` = %s, `part_number` = %s, `van_number` = %s WHERE `id` = %s'

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
