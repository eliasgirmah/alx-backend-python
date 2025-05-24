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

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = connection
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            pass  # Django handles closing
    return wrapper

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
