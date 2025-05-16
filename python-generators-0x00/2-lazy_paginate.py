!/usr/bin/python3
"""Lazy loading paginated data from user_data table."""

import os
import mysql.connector
from dotenv import load_dotenv
import sys

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

def paginate_users(page_size, offset):
    """Fetch a single page of users using LIMIT and OFFSET."""
    connection = connect_to_prodev()
    if connection is None:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """Generator that lazily yields pages of users."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    try:
        for page in lazy_pagination(10):  # Fetch 10 users per page
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()
