
class credential_model:
    def __init__(self, database_conection, credential_table):
        self.connection = database_conection
        self.credential_table = credential_table
        self.cursor = None

    def insert_credential(self, credential: str, registration_number: str, user_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO {self.credential_table} (credential, registration_number, user_name) VALUES (?,?,?)", (credential,registration_number,user_name))
        self.connection.commit()

    def update_credential(self, credential: str, registration_number: str, user_name: str):
        cursor = self.connection.cursor()
        cursor.execute(f"UPDATE {self.credential_table} SET registration_number=?, user_name=? WHERE credential=?", (registration_number, user_name, credential))
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

