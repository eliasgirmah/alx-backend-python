import functools
import logging
import sqlite3
import os
from django.conf import settings
logger = logging.getLogger('user_queries')

def log_queries(query):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Executing query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')  # Adjust if using a different DB
        conn = sqlite3.connect(db_path)
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper