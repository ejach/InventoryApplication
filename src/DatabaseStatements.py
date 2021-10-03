class DatabaseStatements:

    def __init__(self):
        self.select = 'SELECT * FROM parts.parts'
        self.insert = 'INSERT INTO parts.parts (name, part_number) VALUES (%s, %s)'

    def get_select_stmt(self):
        return self.select

    def get_insert_statement(self):
        return self.insert
