import sqlite3
import functools

# Global cache
query_cache = {}

# Decorator to handle DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('mydatabase.db')  # Replace with your DB path
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# ✅ Your cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if query in query_cache:
            print("🔁 Using cached result for query:", query)
            return query_cache[query]

        print("📡 Executing new query:", query)
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# ✅ Function that uses both decorators
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# 👇 First call - not cached
users = fetch_users_with_cache(query="SELECT * FROM users")

# 👇 Second call - cached
users_again = fetch_users_with_cache(query="SELECT * FROM users")
