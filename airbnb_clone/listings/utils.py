from .decorators import log_queries, with_db_connection, transactional, retry_on_failure


# Logging a raw SQL query using Django ORM's raw query capability
@log_queries("SELECT * FROM auth_user")
def get_users_query():
    from django.contrib.auth.models import User
    return User.objects.raw("SELECT * FROM auth_user")


# Auto-handled DB connection to fetch user by ID
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_user WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Transactionally update user's email
@transactional
def update_user_email(cursor, user_id, new_email):
    cursor.execute(
        "UPDATE auth_user SET email = %s WHERE id = %s",
        [new_email, user_id]
    )


# Fetch users from custom table `users` with retries and DB connection
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
