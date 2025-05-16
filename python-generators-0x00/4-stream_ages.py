#!/usr/bin/python3
"""Memory-Efficient Aggregation with Generators."""

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_to_prodev():
    """Connect to the MySQL database using env variables."""
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

def stream_user_ages():
    """Generator that yields one user age at a time."""
    connection = connect_to_prodev()
    if connection is None:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    # Yield one age at a time
    for row in cursor:
        if row['age'] is not None:
            yield row['age']

    cursor.close()
    connection.close()

def calculate_average_age():
    """Calculate average age using the generator."""
    total_age = 0
    count = 0

    # Only one loop here, iterating over generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0
    return total_age / count

if __name__ == "__main__":
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age:.2f}")
