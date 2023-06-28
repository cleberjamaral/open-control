import sqlite3

class credential_model:
    def __init__(self, database_name, credential_table):
        self.database_name = database_name
        self.credential_table = credential_table
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.credential_table} (credential TEXT, registration_number TEXT, user_name TEXT)")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def insert_credential(self, credential: str, registration_number: str, user_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO {self.credential_table} (credential, registration_number, user_name) VALUES (?,?,?)", (credential,registration_number,user_name))
        self.connection.commit()

    def get_all_credentials(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT credential, registration_number, user_name FROM {self.credential_table}")
        credentials = cursor.fetchall()
        return [{'registration_number':credential[1],'user_name':credential[2],'credential':credential[0]} for credential in credentials]
    
    def check_credential_exists(self,credential):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT credential, registration_number, user_name FROM {self.credential_table} WHERE credential = '"+credential+"'")
        credentials = cursor.fetchall()
        return credentials

    def delete_credential(self,credential):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {self.credential_table} WHERE credential = '"+credential+"'")
            self.connection.commit()
            return True
        except Exception as e:
            return False

