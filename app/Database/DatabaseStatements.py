class DatabaseStatements:

    def __init__(self):
        self.select = 'SELECT * FROM parts.parts'
        self.select_vans = 'SELECT * FROM parts.parts WHERE `van_number` = %s'
        self.select_vans_distinct = 'SELECT `van_number` FROM vans.vans ORDER BY van_number'
        self.insert_van = 'INSERT INTO vans.vans (van_number) VALUE (%s)'
        self.insert = 'INSERT INTO parts.parts (name, part_number, van_number) VALUES (%s, %s, %s)'
        self.delete = 'DELETE FROM parts.parts WHERE `id` = %s'
        self.update = 'UPDATE parts.parts set `name` = %s, `part_number` = %s, `van_number` = %s WHERE `id` = %s'

    def get_select_statement(self):
        return self.select

    def get_select_vans_statement(self):
        return self.select_vans

    def get_select_vans_distinct_statement(self):
        return self.select_vans_distinct

    def get_insert_statement(self):
        return self.insert

    def get_insert_van(self):
        return self.insert_van

    def get_delete_statement(self):
        return self.delete

    def get_update_statement(self):
        return self.update
