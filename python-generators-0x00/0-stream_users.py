import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',  # explicitly specify TCP host to avoid named pipe issues
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# your generator function and other code...

def stream_users():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # dictionary=True to get dicts instead of tuples
    
    cursor.execute("SELECT * FROM user_data")
    
    for row in cursor:
        yield row  # yield one row at a time
    
    cursor.close()
    connection.close()

if __name__ == "__main__":
    gen = stream_users()
    for i, user in enumerate(gen):
        print(user)
        if i >= 5:
            break  # print only first 6 users
