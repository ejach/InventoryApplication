class DatabaseStatements:

    def __init__(self):
        self.select = 'SELECT * FROM parts.parts'
        self.select_vans = 'SELECT * FROM parts.parts WHERE `van_number` = %s'
        self.insert = 'INSERT INTO parts.parts (name, part_number, van_number) VALUES (%s, %s, %s)'
        self.delete = 'DELETE FROM parts.parts WHERE `id` = %s'
        self.update = 'UPDATE parts.parts set `name` = %s, `part_number` = %s, `van_number` = %s WHERE `id` = %s'

    def get_select_statement(self):
        return self.select

    def get_select_vans_statement(self):
        return self.select_vans

    def get_insert_statement(self):
        return self.insert

    def get_delete_statement(self):
        return self.delete

    def get_update_statement(self):
        return self.update
