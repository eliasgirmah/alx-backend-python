from .decorators import log_queries
from .decorators import with_db_connection
@log_queries("SELECT * FROM auth_user")
def get_users_query():
    # your query code here
    ...


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_user WHERE id = ?", (user_id,))
    return cursor.fetchone()