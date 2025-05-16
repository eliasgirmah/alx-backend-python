!/usr/bin/python3
# This script connects to the MySQL database and creates a table if it doesn't exist.
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

# Generator: stream_users_in_batches(batch_size) 
# This function streams users from the database in batches of size batch_size.
def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    if connection is None:
        return  # Or raise an exception

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

# Function: batch_processing(batch_size)
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age') and user['age'] > 25:
                print(user)

# Example usage
if __name__ == "__main__":
    batch_size = 10  # Adjust the batch size as needed
    batch_processing(batch_size)