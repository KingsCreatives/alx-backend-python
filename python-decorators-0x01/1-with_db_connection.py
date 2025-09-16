import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to handle database connections automatically.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    return wrapper

def setup_database():
    """
    Creates a sample SQLite database and a users table.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (2, 'Bob')")
    conn.commit()
    conn.close()

setup_database()

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user by ID using a database connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

user = get_user_by_id(user_id=1)
print(user)