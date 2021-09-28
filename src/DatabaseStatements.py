class DatabaseStatements:

    def __init__(self):
        self.select = 'SELECT * FROM parts'
        self.insert = 'INSERT INTO parts (name, part_number) VALUES (?, ?)'

    def get_select_stmt(self):
        return self.select

    def get_insert_statement(self):
        return self.insert
