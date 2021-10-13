class DatabaseStatements:

    def __init__(self):
        self.select = 'SELECT * FROM parts.parts'
        self.insert = 'INSERT INTO parts.parts (name, part_number) VALUES (%s, %s)'
        self.delete = 'DELETE FROM parts.parts WHERE `id` = %s'
        self.update = 'UPDATE parts.parts set `name` = %s, `part_number` = %s WHERE `id` = %s'

    def get_select_stmt(self):
        return self.select

    def get_insert_statement(self):
        return self.insert

    def get_delete_statement(self):
        return self.delete

    def get_update_statement(self):
        return self.update
