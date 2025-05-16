import mysql.connector
from mysql.connector import errorcode
import uuid  # import uuid module to generate UUIDs

def connect_db():
    """Connect to MySQL server (no specific database)"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='elias'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it does not exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        print("Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

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
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create the user_data table"""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    cursor.close()

def insert_data(connection, csv_file):
    import csv
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Generate a new UUID for user_id for each row
                user_id = str(uuid.uuid4())
                cursor.execute(
                    """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, row['name'], row['email'], row['age'])
                )
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data(conn, './data.csv')
        conn.close()
