from .decorators import log_queries, with_db_connection, transactional

# Example: Logging raw SQL query
@log_queries("SELECT * FROM auth_user")
def get_users_query():
    from django.contrib.auth.models import User
    return User.objects.raw("SELECT * FROM auth_user")


# Example: Auto-handled DB connection
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_user WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example: Transactionally update user email
@transactional
def update_user_email(cursor, user_id, new_email):
    cursor.execute("UPDATE auth_user SET email = %s WHERE id = %s", [new_email, user_id])
