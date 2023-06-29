import sqlite3

class event_model:
    def __init__(self, database_name, event_table):
        self.database_name = database_name
        self.event_table = event_table
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.event_table} (date TEXT, credential TEXT, user_name TEXT, event_type TEXT)")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def insert_event(self, date: str, credential: str, user_name: str, event_type: str):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO {self.event_table} (date, credential, user_name, event_type) VALUES (?,?,?,?)", (date,credential,user_name,event_type))
        self.connection.commit()

    def get_all_events(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT date, credential, user_name, event_type FROM {self.event_table}")
        events = cursor.fetchall()
        return [{'date':e[0],'credential':e[1],'user_name':e[2],'event_type':e[3]} for e in events]
    

