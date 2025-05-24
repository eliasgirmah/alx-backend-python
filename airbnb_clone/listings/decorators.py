import functools
import logging
import sqlite3
import os
from django.conf import settings
logger = logging.getLogger('user_queries')
# listings/decorators.py
from functools import wraps
from datetime import datetime
from django.db import connection

def log_queries(query_text):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{datetime.now()}] Executing query: {query_text}")
            return func(*args, **kwargs)
        return wrapper
    return decorator



def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with connection.cursor() as cursor:
            try:
                print("[TRANSACTION] BEGIN")
                result = func(cursor, *args, **kwargs)
                connection.commit()
                print("[TRANSACTION] COMMIT")
                return result
            except Exception as e:
                connection.rollback()
                print("[TRANSACTION] ROLLBACK")
                print(f"[ERROR] {e}")
                raise
    return wrapper

import time
import functools
import sqlite3

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Adjust your DB path as needed or use Django's connection if preferred
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"Attempt {attempts} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            # Final attempt - will raise exception if fails
            return func(*args, **kwargs)
        return wrapper
    return decorator
