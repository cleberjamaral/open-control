class event_model:
    def __init__(self, connection, event_table):
        self.connection = connection
        self.event_table = event_table

    def insert_event(self, credential: str, user_name: str, event_type: str):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO {self.event_table} (date, credential, user_name, event_type) VALUES (datetime('now'),?,?,?)", (credential,user_name,event_type))
        self.connection.commit()

    def get_all_events(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT date, credential, user_name, event_type FROM {self.event_table} ORDER BY date DESC")
        events = cursor.fetchall()
        return [{'date':e[0],'credential':e[1],'user_name':e[2],'event_type':e[3]} for e in events]
    

