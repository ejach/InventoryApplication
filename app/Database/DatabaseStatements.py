from app.Database.DatabaseConnector import DatabaseConnector


class DatabaseStatements:
    def __init__(self):
        self.dbc = DatabaseConnector()
        self.db = self.dbc.get_db()
        self.select = f'SELECT * FROM {self.db}.parts'
        self.select_vans = f'SELECT * FROM {self.db}.parts WHERE `van_number` = %s'
        self.select_vans_order = f'SELECT * FROM {self.db}.vans ORDER BY LENGTH(van_number), van_number'
        self.select_vans_distinct = f'SELECT DISTINCT `van_number` from {self.db}.parts ORDER BY `van_number`'
        self.select_vans_dupes = f'SELECT `van_number` from {self.db}.vans'
        self.select_parts_by_van = f'SELECT `id`, `name`, `amount`, `part_number` FROM {self.db}.parts WHERE ' \
                                   f'`van_number` = %s'
        self.select_total_amount_by_van = f'SELECT SUM(amount) FROM {self.db}.parts WHERE `van_number` = %s;'
        self.insert_job = f'INSERT INTO {self.db}.jobs (username, time, van_number, parts_used) VALUES ' \
                          f'(LOWER(%s), %s, %s, %s)'
        self.get_jobs = f'SELECT * FROM {self.db}.jobs'
        self.update_part_amount_by_van = f'UPDATE {self.db}.parts SET `amount` = %s WHERE `id` = %s'
        self.insert_van = f'INSERT INTO {self.db}.vans (van_number) VALUE (%s)'
        self.delete_van = f'DELETE FROM {self.db}.vans WHERE `id` = %s'
        self.update_van = f'UPDATE {self.db}.vans SET `van_number` = %s WHERE `id` = %s'
        self.login = f'SELECT * FROM {self.db}.accounts WHERE LOWER(`username`) = %s AND LOWER(`password`) = %s'
        self.register = f'INSERT INTO {self.db}.accounts (username, password) VALUES (LOWER(%s), %s)'
        self.check_admin = f'SELECT is_admin FROM {self.db}.accounts WHERE `username` = LOWER(%s)'
        self.check_confirmed = f'SELECT is_confirmed FROM {self.db}.accounts WHERE `username` = LOWER(%s)'
        self.confirm_account = f'UPDATE {self.db}.accounts SET `is_confirmed` = 1 WHERE `id` = %s'
        self.modify_admin = f'UPDATE {self.db}.accounts SET `is_admin` = %s WHERE `id` = %s'
        self.delete_account = f'DELETE FROM {self.db}.accounts WHERE `id` = %s'
        self.get_users = f'SELECT id, LOWER(username), is_admin, is_confirmed FROM {self.db}.accounts ' \
                         f'WHERE username != LOWER(%s)'
        self.modify_thresh = f'UPDATE {self.db}.parts SET low_thresh = %s WHERE id = %s'
        self.low_parts = f'SELECT * FROM {self.db}.parts WHERE low_thresh > amount'
        self.check_if_username_exists = f'SELECT * FROM {self.db}.accounts WHERE `username` = LOWER(%s)'
        self.get_password_by_username = f'SELECT `password` FROM {self.db}.accounts WHERE `username` = LOWER(%s)'
        self.insert = f'INSERT INTO {self.db}.parts (name, amount, part_number, van_number) VALUES (%s, %s, %s, %s)'
        self.delete = f'DELETE FROM {self.db}.parts WHERE `id` = %s'
        self.select_part_by_id = f'SELECT * FROM {self.db}.parts WHERE `id` = %s'
        self.update = f'UPDATE {self.db}.parts set `name` = %s, `amount` = %s, `part_number` = %s, `van_number` = %s ' \
                      f'WHERE `id` = %s'

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

    def get_modify_admin(self):
        return self.modify_admin

    def get_select_parts_by_van(self):
        return self.select_parts_by_van

    def get_update_part_amount_by_van(self):
        return self.update_part_amount_by_van

    def get_select_total_amount_by_van(self):
        return self.select_total_amount_by_van

    def get_select_part_by_id(self):
        return self.select_part_by_id

    def get_modify_thresh(self):
        return self.modify_thresh

    def get_low_parts(self):
        return self.low_parts
