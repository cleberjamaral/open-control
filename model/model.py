import sqlite3

class CardModel:
    def __init__(self, database_name, table_name):
        self.database_name = database_name
        self.table_name = table_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (card_number TEXT)")

    def insert_card_number(self, card_number):
        self.cursor.execute(f"INSERT INTO {self.table_name} (card_number) VALUES (?)", (card_number,))
        self.conn.commit()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()