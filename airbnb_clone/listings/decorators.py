import functools
import logging

logger = logging.getLogger('user_queries')

def log_queries(query):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Executing query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
