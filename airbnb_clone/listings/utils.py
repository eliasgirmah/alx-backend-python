from .decorators import log_queries

@log_queries("SELECT * FROM auth_user")
def get_users_query():
    # your query code here
    ...
