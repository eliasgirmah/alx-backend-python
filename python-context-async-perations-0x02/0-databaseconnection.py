# 0-databaseconnection.py

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # returned to the 'as' part in with statement

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Using the context manager
if __name__ == "__main__":
    with DatabaseConnection("my_database.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(user)
