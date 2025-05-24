import sqlite3
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open the connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection to the decorated function
            result = func(conn, *args, **kwargs)
        finally:
            # Always close connection even if func raises an exception
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user with ID=1
user = get_user_by_id(user_id=1)
print(user)
