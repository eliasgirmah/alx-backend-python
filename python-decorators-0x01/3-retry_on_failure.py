import time
import sqlite3
import functools

# 1. Decorator to automatically open and close DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # change path if needed
        try:
            return func(conn, *args, **kwargs)  # pass conn as first arg
        finally:
            conn.close()
    return wrapper

# 2. Decorator factory for retrying on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)  # try the function
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            # Final attempt, let exception raise if fails
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 3. Use both decorators on a DB function
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# 4. Test the function
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
