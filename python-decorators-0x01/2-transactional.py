import sqlite3 
import functools

"""your code goes here"""
def transactional(func):
    @functools.wraps(func)

    def wrapper(conn,*args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper


      
    


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
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # We add an 'email' column to the 'users' table if it doesn't exist.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (2, 'Bob')")
    conn.commit()
    conn.close()

setup_database()

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("User 1's email updated.")


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch and print the updated user to verify the change.
user = get_user_by_id(user_id=1)
print(f"Updated user: {user}")